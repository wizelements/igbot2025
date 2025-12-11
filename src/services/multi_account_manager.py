"""
Multi-account manager supporting 10-10,000 accounts with session recovery,
2FA/challenge solving, and intelligent warmup curves
"""
import asyncio
import json
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import pyotp
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, ChallengeRequired, TwoFactorRequired,
    PleaseWaitFewMinutes, RateLimitError
)
from loguru import logger
import random

from src.config import config
from src.services.proxy_rotator import proxy_rotator, Proxy


class AccountStatus(Enum):
    INACTIVE = "inactive"
    WARMING_UP = "warming_up"
    ACTIVE = "active"
    PAUSED = "paused"
    BANNED = "banned"
    CHALLENGE = "challenge"
    RATE_LIMITED = "rate_limited"


@dataclass
class AccountSession:
    username: str
    password: str
    twofa_secret: str = ""
    
    # Session state
    client: Optional[Client] = None
    proxy: Optional[Proxy] = None
    status: AccountStatus = AccountStatus.INACTIVE
    
    # Session persistence
    session_file: Path = None
    last_login: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    
    # Warmup tracking
    created_date: datetime = field(default_factory=datetime.now)
    warmup_day: int = 0
    warmup_complete: bool = False
    
    # Statistics
    total_follows: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_posts: int = 0
    
    # Risk management
    ban_risk_score: float = 0.0
    challenge_count: int = 0
    rate_limit_count: int = 0
    last_ban_check: Optional[datetime] = None
    
    # Performance
    success_count: int = 0
    error_count: int = 0
    
    def __post_init__(self):
        if not self.session_file:
            self.session_file = Path(f"sessions/{self.username}.json")
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.error_count
        if total == 0:
            return 1.0
        return self.success_count / total
    
    @property
    def is_healthy(self) -> bool:
        """Check if account is healthy for operations"""
        if self.status in [AccountStatus.BANNED, AccountStatus.RATE_LIMITED]:
            return False
        if self.ban_risk_score > config.emergency.max_ban_risk_score:
            return False
        return self.success_rate > config.emergency.min_success_rate
    
    def calculate_warmup_limits(self) -> Dict[str, int]:
        """Calculate action limits based on warmup day"""
        if self.warmup_complete:
            return {
                'follows': config.anti_ban.max_follows_per_day,
                'likes': config.anti_ban.max_likes_per_day,
                'comments': config.anti_ban.max_comments_per_day,
            }
        
        # Progressive warmup curve
        warmup_days = config.anti_ban.warmup_period_days
        progress = min(self.warmup_day / warmup_days, 1.0)
        
        # Exponential curve for natural growth
        curve = progress ** 0.5
        
        return {
            'follows': int(config.anti_ban.max_follows_per_day * curve * 0.3),  # Start at 30%
            'likes': int(config.anti_ban.max_likes_per_day * curve * 0.5),     # Start at 50%
            'comments': int(config.anti_ban.max_comments_per_day * curve * 0.2),  # Start at 20%
        }


class MultiAccountManager:
    """
    Manages multiple Instagram accounts with session persistence,
    2FA handling, challenge solving, and warmup management
    """
    
    def __init__(self):
        self.accounts: Dict[str, AccountSession] = {}
        self.session_dir = Path("sessions")
        self.session_dir.mkdir(exist_ok=True)
        self._locks: Dict[str, asyncio.Lock] = {}
    
    async def initialize(self):
        """Initialize all accounts"""
        logger.info(f"Initializing multi-account manager with {len(config.IG_ACCOUNTS)} accounts")
        
        # Create account sessions
        for account_data in config.IG_ACCOUNTS:
            username = account_data['username']
            session = AccountSession(
                username=username,
                password=account_data['password'],
                twofa_secret=account_data.get('2fa_secret', '')
            )
            self.accounts[username] = session
            self._locks[username] = asyncio.Lock()
        
        # Load existing sessions
        await self._load_all_sessions()
        
        # Login to all accounts
        await self._login_all_accounts()
        
        logger.success(f"Multi-account manager initialized with {len(self.accounts)} accounts")
    
    async def _load_all_sessions(self):
        """Load all existing sessions from disk"""
        for username, session in self.accounts.items():
            try:
                await self._load_session(session)
            except Exception as e:
                logger.debug(f"Could not load session for {username}: {e}")
    
    async def _load_session(self, session: AccountSession):
        """Load a single account session"""
        if not session.session_file.exists():
            return
        
        try:
            # Load session data
            with open(session.session_file, 'r') as f:
                data = json.load(f)
            
            # Restore session state
            session.last_login = datetime.fromisoformat(data.get('last_login', ''))
            session.last_activity = datetime.fromisoformat(data.get('last_activity', ''))
            session.warmup_day = data.get('warmup_day', 0)
            session.warmup_complete = data.get('warmup_complete', False)
            session.total_follows = data.get('total_follows', 0)
            session.total_likes = data.get('total_likes', 0)
            session.total_comments = data.get('total_comments', 0)
            session.ban_risk_score = data.get('ban_risk_score', 0.0)
            
            # Restore Instagram client session
            if 'client_settings' in data:
                client = Client()
                client.set_settings(data['client_settings'])
                session.client = client
                session.status = AccountStatus.ACTIVE
                logger.info(f"Restored session for {session.username}")
            
        except Exception as e:
            logger.warning(f"Failed to load session for {session.username}: {e}")
    
    async def _save_session(self, session: AccountSession):
        """Save account session to disk"""
        try:
            data = {
                'username': session.username,
                'last_login': session.last_login.isoformat() if session.last_login else None,
                'last_activity': session.last_activity.isoformat() if session.last_activity else None,
                'warmup_day': session.warmup_day,
                'warmup_complete': session.warmup_complete,
                'total_follows': session.total_follows,
                'total_likes': session.total_likes,
                'total_comments': session.total_comments,
                'ban_risk_score': session.ban_risk_score,
            }
            
            # Save Instagram client settings
            if session.client:
                data['client_settings'] = session.client.get_settings()
            
            with open(session.session_file, 'w') as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to save session for {session.username}: {e}")
    
    async def _login_all_accounts(self):
        """Login to all accounts concurrently"""
        tasks = [self.login_account(username) for username in self.accounts.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success = sum(1 for r in results if r is True)
        failed = len(results) - success
        
        logger.info(f"Account login complete: {success} successful, {failed} failed")
    
    async def login_account(self, username: str) -> bool:
        """
        Login to an account with full 2FA and challenge handling
        """
        async with self._locks[username]:
            session = self.accounts.get(username)
            if not session:
                logger.error(f"Account {username} not found")
                return False
            
            # Check if already logged in
            if session.client and session.status == AccountStatus.ACTIVE:
                try:
                    # Verify session is still valid
                    session.client.get_timeline_feed()
                    logger.debug(f"Account {username} already logged in")
                    return True
                except LoginRequired:
                    logger.info(f"Session expired for {username}, re-logging in")
            
            try:
                # Create new client
                client = Client()
                client.delay_range = [1, 3]
                
                # Set proxy
                proxy = await proxy_rotator.get_proxy(account_username=username)
                if proxy:
                    client.set_proxy(proxy.url)
                    session.proxy = proxy
                
                # Attempt login
                logger.info(f"Logging in account {username}")
                
                try:
                    client.login(session.username, session.password)
                    
                except TwoFactorRequired:
                    # Handle 2FA
                    if session.twofa_secret:
                        totp = pyotp.TOTP(session.twofa_secret)
                        code = totp.now()
                        logger.info(f"Using 2FA code for {username}")
                        client.login(session.username, session.password, verification_code=code)
                    else:
                        logger.error(f"2FA required for {username} but no secret provided")
                        session.status = AccountStatus.CHALLENGE
                        return False
                
                except ChallengeRequired as e:
                    # Handle challenge
                    logger.warning(f"Challenge required for {username}: {e}")
                    session.status = AccountStatus.CHALLENGE
                    session.challenge_count += 1
                    
                    # Attempt auto-challenge resolution
                    try:
                        await self._solve_challenge(client, session)
                    except Exception as ce:
                        logger.error(f"Challenge solving failed for {username}: {ce}")
                        return False
                
                # Success
                session.client = client
                session.status = AccountStatus.ACTIVE
                session.last_login = datetime.now()
                session.success_count += 1
                
                # Save session
                await self._save_session(session)
                
                logger.success(f"Successfully logged in {username}")
                return True
                
            except PleaseWaitFewMinutes:
                logger.warning(f"Rate limited during login for {username}")
                session.status = AccountStatus.RATE_LIMITED
                session.rate_limit_count += 1
                return False
            
            except Exception as e:
                logger.error(f"Login failed for {username}: {e}")
                session.error_count += 1
                session.status = AccountStatus.INACTIVE
                return False
    
    async def _solve_challenge(self, client: Client, session: AccountSession):
        """Auto-solve Instagram challenges"""
        logger.info(f"Attempting to solve challenge for {session.username}")
        
        # Get challenge info
        challenge_info = client.challenge_resolve()
        
        if challenge_info.get('step_name') == 'verify_email':
            # Email verification
            client.challenge_resolve_email()
            logger.info(f"Email verification challenge sent for {session.username}")
        
        elif challenge_info.get('step_name') == 'verify_phone':
            # Phone verification
            client.challenge_resolve_phone()
            logger.info(f"Phone verification challenge sent for {session.username}")
        
        # Note: Full challenge solving requires user interaction
        # In production, integrate with SMS/email services
    
    async def get_client(self, username: str) -> Optional[Client]:
        """
        Get Instagram client for an account, ensuring it's logged in
        """
        session = self.accounts.get(username)
        if not session:
            return None
        
        # Ensure logged in
        if not session.client or session.status != AccountStatus.ACTIVE:
            await self.login_account(username)
        
        if session.client and session.status == AccountStatus.ACTIVE:
            session.last_activity = datetime.now()
            return session.client
        
        return None
    
    async def perform_action(
        self,
        username: str,
        action_type: str,
        action_func: callable,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """
        Safely perform an action with error handling and tracking
        """
        session = self.accounts.get(username)
        if not session:
            return None
        
        # Check if account is healthy
        if not session.is_healthy:
            logger.warning(f"Account {username} is not healthy, skipping action")
            return None
        
        # Check warmup limits
        limits = session.calculate_warmup_limits()
        action_map = {
            'follow': session.total_follows,
            'like': session.total_likes,
            'comment': session.total_comments,
        }
        
        if action_type in action_map and action_type in limits:
            if action_map[action_type] >= limits[action_type]:
                logger.debug(f"Daily limit reached for {action_type} on {username}")
                return None
        
        # Get client
        client = await self.get_client(username)
        if not client:
            return None
        
        try:
            # Perform action
            result = await asyncio.to_thread(action_func, client, *args, **kwargs)
            
            # Update statistics
            session.success_count += 1
            
            if action_type == 'follow':
                session.total_follows += 1
            elif action_type == 'like':
                session.total_likes += 1
            elif action_type == 'comment':
                session.total_comments += 1
            elif action_type == 'post':
                session.total_posts += 1
            
            # Update warmup progress
            if not session.warmup_complete:
                days_since_created = (datetime.now() - session.created_date).days
                session.warmup_day = days_since_created
                if session.warmup_day >= config.anti_ban.warmup_period_days:
                    session.warmup_complete = True
                    logger.success(f"Account {username} warmup complete!")
            
            # Save session
            await self._save_session(session)
            
            return result
            
        except RateLimitError:
            logger.warning(f"Rate limit hit for {username}")
            session.status = AccountStatus.RATE_LIMITED
            session.rate_limit_count += 1
            session.ban_risk_score += 10
            return None
        
        except ChallengeRequired:
            logger.warning(f"Challenge triggered for {username}")
            session.status = AccountStatus.CHALLENGE
            session.challenge_count += 1
            session.ban_risk_score += 20
            return None
        
        except Exception as e:
            logger.error(f"Action failed for {username}: {e}")
            session.error_count += 1
            session.ban_risk_score += 5
            return None
    
    def get_account_stats(self, username: str) -> Dict:
        """Get statistics for an account"""
        session = self.accounts.get(username)
        if not session:
            return {}
        
        warmup_limits = session.calculate_warmup_limits()
        
        return {
            'username': username,
            'status': session.status.value,
            'is_healthy': session.is_healthy,
            'ban_risk_score': session.ban_risk_score,
            'success_rate': round(session.success_rate, 4),
            'last_login': session.last_login.isoformat() if session.last_login else None,
            'last_activity': session.last_activity.isoformat() if session.last_activity else None,
            'warmup_day': session.warmup_day,
            'warmup_complete': session.warmup_complete,
            'warmup_limits': warmup_limits,
            'total_actions': {
                'follows': session.total_follows,
                'likes': session.total_likes,
                'comments': session.total_comments,
                'posts': session.total_posts,
            },
            'errors': {
                'challenge_count': session.challenge_count,
                'rate_limit_count': session.rate_limit_count,
            }
        }
    
    def get_all_stats(self) -> List[Dict]:
        """Get statistics for all accounts"""
        return [self.get_account_stats(username) for username in self.accounts.keys()]
    
    async def pause_account(self, username: str):
        """Pause an account"""
        session = self.accounts.get(username)
        if session:
            session.status = AccountStatus.PAUSED
            logger.info(f"Paused account {username}")
    
    async def resume_account(self, username: str):
        """Resume an account"""
        session = self.accounts.get(username)
        if session:
            session.status = AccountStatus.ACTIVE
            logger.info(f"Resumed account {username}")
    
    async def shutdown(self):
        """Shutdown all accounts and save sessions"""
        logger.info("Shutting down multi-account manager")
        
        # Save all sessions
        tasks = [self._save_session(session) for session in self.accounts.values()]
        await asyncio.gather(*tasks)
        
        logger.success("All sessions saved")


# Global account manager instance
account_manager = MultiAccountManager()
