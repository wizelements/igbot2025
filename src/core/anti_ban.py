"""
Advanced anti-ban system with human simulation, shadowban detection, and anomaly detection
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger
import numpy as np

from src.config import config


@dataclass
class ActionHistory:
    """Track action history for pattern analysis"""
    username: str
    action_type: str
    timestamp: datetime
    success: bool
    delay_before: float
    
    
@dataclass
class AccountHealth:
    """Health metrics for an account"""
    username: str
    shadowban_detected: bool = False
    last_shadowban_check: Optional[datetime] = None
    action_history: List[ActionHistory] = field(default_factory=list)
    
    # Pattern metrics
    avg_delay: float = 0.0
    action_variance: float = 0.0
    peak_hour_ratio: float = 0.0
    
    # Risk scores
    ban_risk_score: float = 0.0
    anomaly_score: float = 0.0
    
    # Counters
    failed_actions_streak: int = 0
    successful_actions_streak: int = 0


class AntiBanSystem:
    """
    Advanced anti-ban system with:
    - Human-like delays with variance
    - Action pattern randomization
    - Shadowban detection
    - Anomaly detection and auto-pause
    - Behavioral simulation
    """
    
    def __init__(self):
        self.account_health: Dict[str, AccountHealth] = {}
        self.monitoring_task: Optional[asyncio.Task] = None
    
    async def initialize(self):
        """Initialize anti-ban system"""
        logger.info("Initializing anti-ban system")
        
        # Create health tracking for all accounts
        from src.services.multi_account_manager import account_manager
        for username in account_manager.accounts.keys():
            self.account_health[username] = AccountHealth(username=username)
        
        # Start monitoring
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        logger.success("Anti-ban system initialized")
    
    async def apply_human_delay(
        self,
        username: str,
        action_type: str = 'default'
    ) -> float:
        """
        Apply human-like delay with realistic variance
        
        Returns: delay applied in seconds
        """
        # Get base delay from scheduler
        from src.services.scheduler import global_scheduler
        acc_scheduler = global_scheduler.account_schedulers.get(username)
        
        if acc_scheduler:
            base_delay = acc_scheduler.get_next_action_delay()
        else:
            base_delay = random.randint(
                config.anti_ban.min_delay_seconds,
                config.anti_ban.max_delay_seconds
            )
        
        # Apply action-specific multipliers
        action_multipliers = {
            'follow': 1.0,
            'like': 0.7,
            'comment': 1.5,  # Comments are more sensitive
            'unfollow': 1.2,
            'post': 2.0,
        }
        
        multiplier = action_multipliers.get(action_type, 1.0)
        adjusted_delay = base_delay * multiplier
        
        # Add human variance (normal distribution)
        variance = config.anti_ban.action_variance
        variance_amount = random.gauss(0, variance)
        final_delay = adjusted_delay * (1 + variance_amount)
        
        # Add random micro-delays (typing, thinking)
        micro_delays = [0.3, 0.5, 0.8, 1.2, 1.5]
        if random.random() < 0.3:  # 30% chance
            final_delay += random.choice(micro_delays)
        
        # Ensure within bounds
        final_delay = max(
            config.anti_ban.min_delay_seconds,
            min(final_delay, config.anti_ban.max_delay_seconds * 2)
        )
        
        logger.debug(f"[{username}] Applying delay: {final_delay:.1f}s for {action_type}")
        await asyncio.sleep(final_delay)
        
        return final_delay
    
    async def track_action(
        self,
        username: str,
        action_type: str,
        success: bool,
        delay_before: float
    ):
        """Track action for pattern analysis"""
        health = self.account_health.get(username)
        if not health:
            return
        
        # Add to history
        history_entry = ActionHistory(
            username=username,
            action_type=action_type,
            timestamp=datetime.now(),
            success=success,
            delay_before=delay_before
        )
        health.action_history.append(history_entry)
        
        # Keep only recent history (last 1000 actions)
        if len(health.action_history) > 1000:
            health.action_history = health.action_history[-1000:]
        
        # Update streaks
        if success:
            health.successful_actions_streak += 1
            health.failed_actions_streak = 0
        else:
            health.failed_actions_streak += 1
            health.successful_actions_streak = 0
        
        # Update metrics
        await self._update_health_metrics(username)
    
    async def _update_health_metrics(self, username: str):
        """Update health metrics for an account"""
        health = self.account_health.get(username)
        if not health or not health.action_history:
            return
        
        recent_actions = health.action_history[-100:]  # Last 100 actions
        
        # Calculate average delay
        delays = [a.delay_before for a in recent_actions]
        health.avg_delay = np.mean(delays)
        health.action_variance = np.std(delays)
        
        # Calculate success rate
        successes = sum(1 for a in recent_actions if a.success)
        success_rate = successes / len(recent_actions)
        
        # Calculate ban risk score
        risk_score = 0.0
        
        # Low variance = bot-like behavior
        if health.action_variance < 5.0:
            risk_score += 15
        
        # Low success rate
        if success_rate < 0.7:
            risk_score += 20
        
        # Failed action streak
        if health.failed_actions_streak > 5:
            risk_score += 30
        
        # Very high frequency
        if health.avg_delay < 20:
            risk_score += 25
        
        health.ban_risk_score = min(risk_score, 100)
        
        # Detect anomalies
        await self._detect_anomalies(username)
    
    async def _detect_anomalies(self, username: str):
        """Detect anomalous behavior patterns"""
        health = self.account_health.get(username)
        if not health:
            return
        
        anomaly_score = 0.0
        
        # Sudden spike in failures
        if health.failed_actions_streak > 10:
            anomaly_score += 40
            logger.warning(f"[{username}] Anomaly: High failure streak detected")
        
        # Sudden change in patterns
        if len(health.action_history) > 100:
            recent = health.action_history[-20:]
            older = health.action_history[-100:-20]
            
            recent_delays = [a.delay_before for a in recent]
            older_delays = [a.delay_before for a in older]
            
            recent_avg = np.mean(recent_delays)
            older_avg = np.mean(older_delays)
            
            # Large deviation in delay patterns
            if abs(recent_avg - older_avg) > 30:
                anomaly_score += 20
        
        health.anomaly_score = anomaly_score
        
        # Auto-pause if anomaly detected and configured
        if anomaly_score > 50 and config.emergency.auto_pause_on_anomaly:
            logger.error(f"[{username}] High anomaly score ({anomaly_score}), auto-pausing account")
            from src.services.multi_account_manager import account_manager
            await account_manager.pause_account(username)
    
    async def check_shadowban(self, username: str) -> bool:
        """
        Check if account is shadowbanned
        
        Method:
        1. Post with unique hashtag
        2. Check if visible in hashtag search from different account
        3. Check engagement rate drop
        """
        if not config.anti_ban.shadowban_detection:
            return False
        
        health = self.account_health.get(username)
        if not health:
            return False
        
        # Don't check too frequently
        if health.last_shadowban_check:
            time_since_check = datetime.now() - health.last_shadowban_check
            if time_since_check < timedelta(hours=6):
                return health.shadowban_detected
        
        logger.info(f"[{username}] Checking for shadowban")
        
        try:
            from src.services.multi_account_manager import account_manager
            client = await account_manager.get_client(username)
            
            if not client:
                return False
            
            # Method 1: Check recent post engagement
            async def check_engagement(c):
                medias = c.user_medias(c.user_id, amount=10)
                if not medias:
                    return None
                
                recent_engagement = []
                for media in medias:
                    if media.like_count and media.view_count:
                        rate = media.like_count / max(media.view_count, 1)
                        recent_engagement.append(rate)
                
                return np.mean(recent_engagement) if recent_engagement else None
            
            engagement_rate = await asyncio.to_thread(check_engagement, client)
            
            # Shadowban indicators
            shadowban_detected = False
            
            if engagement_rate is not None:
                # Very low engagement rate
                if engagement_rate < 0.01:
                    shadowban_detected = True
                    logger.warning(f"[{username}] Low engagement rate detected: {engagement_rate:.4f}")
            
            # Check hashtag visibility (simplified)
            # In production, use a second account to verify
            
            health.shadowban_detected = shadowban_detected
            health.last_shadowban_check = datetime.now()
            
            if shadowban_detected:
                logger.error(f"[{username}] ⚠️ SHADOWBAN DETECTED ⚠️")
                # Increase ban risk
                health.ban_risk_score = min(health.ban_risk_score + 50, 100)
            else:
                logger.success(f"[{username}] No shadowban detected")
            
            return shadowban_detected
        
        except Exception as e:
            logger.error(f"[{username}] Shadowban check error: {e}")
            return False
    
    async def _monitoring_loop(self):
        """Continuous monitoring of all accounts"""
        logger.info("Starting anti-ban monitoring loop")
        
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                # Check all accounts
                for username in self.account_health.keys():
                    health = self.account_health[username]
                    
                    # Log high risk accounts
                    if health.ban_risk_score > 60:
                        logger.warning(
                            f"[{username}] High ban risk: {health.ban_risk_score:.1f}/100"
                        )
                    
                    # Periodic shadowban check
                    if random.random() < 0.1:  # 10% chance per cycle
                        await self.check_shadowban(username)
                
            except Exception as e:
                logger.error(f"Error in anti-ban monitoring: {e}")
    
    def get_account_health(self, username: str) -> Dict:
        """Get health report for an account"""
        health = self.account_health.get(username)
        if not health:
            return {}
        
        recent_actions = health.action_history[-50:] if health.action_history else []
        success_rate = sum(1 for a in recent_actions if a.success) / max(len(recent_actions), 1)
        
        return {
            'username': username,
            'ban_risk_score': round(health.ban_risk_score, 2),
            'anomaly_score': round(health.anomaly_score, 2),
            'shadowban_detected': health.shadowban_detected,
            'last_shadowban_check': health.last_shadowban_check.isoformat() if health.last_shadowban_check else None,
            'avg_delay_seconds': round(health.avg_delay, 2),
            'action_variance': round(health.action_variance, 2),
            'recent_success_rate': round(success_rate, 4),
            'failed_streak': health.failed_actions_streak,
            'successful_streak': health.successful_actions_streak,
            'total_actions_tracked': len(health.action_history)
        }
    
    def get_all_health(self) -> List[Dict]:
        """Get health reports for all accounts"""
        return [self.get_account_health(username) for username in self.account_health.keys()]
    
    async def shutdown(self):
        """Shutdown anti-ban system"""
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Anti-ban system shut down")


# Global anti-ban system
anti_ban_system = AntiBanSystem()
