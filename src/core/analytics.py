"""
Analytics and metrics tracking system with Prometheus integration
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, field
import json
from pathlib import Path
from loguru import logger
from prometheus_client import Counter, Gauge, Histogram, start_http_server

from src.config import config


@dataclass
class ActionMetrics:
    """Metrics for a specific action type"""
    total: int = 0
    successful: int = 0
    failed: int = 0
    
    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.successful / self.total


@dataclass
class AccountMetrics:
    """Comprehensive metrics for an account"""
    username: str
    
    # Action metrics
    follows: ActionMetrics = field(default_factory=ActionMetrics)
    likes: ActionMetrics = field(default_factory=ActionMetrics)
    comments: ActionMetrics = field(default_factory=ActionMetrics)
    unfollows: ActionMetrics = field(default_factory=ActionMetrics)
    posts: ActionMetrics = field(default_factory=ActionMetrics)
    
    # Growth metrics
    followers_history: deque = field(default_factory=lambda: deque(maxlen=1000))
    following_history: deque = field(default_factory=lambda: deque(maxlen=1000))
    
    # Engagement metrics
    total_likes_received: int = 0
    total_comments_received: int = 0
    avg_engagement_rate: float = 0.0
    
    # Performance
    uptime_seconds: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    
    # Revenue (if applicable)
    estimated_revenue: float = 0.0


class Analytics:
    """
    Advanced analytics system with Prometheus metrics
    """
    
    def __init__(self):
        self.account_metrics: Dict[str, AccountMetrics] = {}
        self.metrics_dir = Path("metrics")
        self.metrics_dir.mkdir(exist_ok=True)
        
        # Prometheus metrics
        self._init_prometheus_metrics()
        
        # Tracking tasks
        self.tracking_task: Optional[asyncio.Task] = None
    
    def _init_prometheus_metrics(self):
        """Initialize Prometheus metrics"""
        # Counters
        self.action_counter = Counter(
            'igbot_actions_total',
            'Total actions performed',
            ['account', 'action_type', 'status']
        )
        
        self.error_counter = Counter(
            'igbot_errors_total',
            'Total errors',
            ['account', 'error_type']
        )
        
        # Gauges
        self.followers_gauge = Gauge(
            'igbot_followers',
            'Current followers count',
            ['account']
        )
        
        self.following_gauge = Gauge(
            'igbot_following',
            'Current following count',
            ['account']
        )
        
        self.ban_risk_gauge = Gauge(
            'igbot_ban_risk_score',
            'Ban risk score (0-100)',
            ['account']
        )
        
        self.engagement_rate_gauge = Gauge(
            'igbot_engagement_rate',
            'Engagement rate',
            ['account']
        )
        
        # Histograms
        self.action_duration_histogram = Histogram(
            'igbot_action_duration_seconds',
            'Action duration in seconds',
            ['account', 'action_type']
        )
    
    async def initialize(self):
        """Initialize analytics system"""
        logger.info("Initializing analytics system")
        
        # Create metrics for all accounts
        from src.services.multi_account_manager import account_manager
        for username in account_manager.accounts.keys():
            self.account_metrics[username] = AccountMetrics(username=username)
        
        # Load historical metrics
        await self._load_all_metrics()
        
        # Start Prometheus server
        if config.monitoring.enable_metrics:
            try:
                start_http_server(config.monitoring.prometheus_port)
                logger.success(f"Prometheus metrics server started on port {config.monitoring.prometheus_port}")
            except Exception as e:
                logger.warning(f"Could not start Prometheus server: {e}")
        
        # Start tracking
        self.tracking_task = asyncio.create_task(self._tracking_loop())
        
        logger.success("Analytics system initialized")
    
    async def track_action(
        self,
        username: str,
        action_type: str,
        success: bool,
        duration: float = 0.0
    ):
        """Track an action"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return
        
        # Get action metrics object
        action_metrics_map = {
            'follow': metrics.follows,
            'like': metrics.likes,
            'comment': metrics.comments,
            'unfollow': metrics.unfollows,
            'post': metrics.posts,
        }
        
        action_metrics = action_metrics_map.get(action_type)
        if action_metrics:
            action_metrics.total += 1
            if success:
                action_metrics.successful += 1
            else:
                action_metrics.failed += 1
        
        # Update Prometheus metrics
        status = 'success' if success else 'failed'
        self.action_counter.labels(
            account=username,
            action_type=action_type,
            status=status
        ).inc()
        
        if duration > 0:
            self.action_duration_histogram.labels(
                account=username,
                action_type=action_type
            ).observe(duration)
    
    async def track_followers(self, username: str, count: int):
        """Track follower count"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return
        
        metrics.followers_history.append({
            'timestamp': datetime.now().isoformat(),
            'count': count
        })
        
        self.followers_gauge.labels(account=username).set(count)
    
    async def track_following(self, username: str, count: int):
        """Track following count"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return
        
        metrics.following_history.append({
            'timestamp': datetime.now().isoformat(),
            'count': count
        })
        
        self.following_gauge.labels(account=username).set(count)
    
    async def track_engagement(self, username: str, rate: float):
        """Track engagement rate"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return
        
        metrics.avg_engagement_rate = rate
        self.engagement_rate_gauge.labels(account=username).set(rate)
    
    async def track_ban_risk(self, username: str, score: float):
        """Track ban risk score"""
        self.ban_risk_gauge.labels(account=username).set(score)
    
    async def _tracking_loop(self):
        """Periodic metrics collection"""
        logger.info("Starting analytics tracking loop")
        
        while True:
            try:
                await asyncio.sleep(60)  # Every minute
                
                # Update metrics for all accounts
                from src.services.multi_account_manager import account_manager
                
                for username in self.account_metrics.keys():
                    try:
                        client = await account_manager.get_client(username)
                        if not client:
                            continue
                        
                        # Get follower/following counts
                        async def get_counts(c):
                            user_info = c.user_info(c.user_id)
                            return {
                                'followers': user_info.follower_count,
                                'following': user_info.following_count,
                                'media': user_info.media_count
                            }
                        
                        counts = await asyncio.to_thread(get_counts, client)
                        
                        await self.track_followers(username, counts['followers'])
                        await self.track_following(username, counts['following'])
                        
                    except Exception as e:
                        logger.debug(f"Error tracking metrics for {username}: {e}")
                
                # Save metrics periodically (every 5 minutes)
                if datetime.now().minute % 5 == 0:
                    await self._save_all_metrics()
                
            except Exception as e:
                logger.error(f"Error in analytics tracking loop: {e}")
    
    async def _save_all_metrics(self):
        """Save all metrics to disk"""
        for username, metrics in self.account_metrics.items():
            await self._save_metrics(username)
    
    async def _save_metrics(self, username: str):
        """Save metrics for an account"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return
        
        try:
            metrics_file = self.metrics_dir / f"{username}_metrics.json"
            
            data = {
                'username': username,
                'follows': {
                    'total': metrics.follows.total,
                    'successful': metrics.follows.successful,
                    'failed': metrics.follows.failed,
                },
                'likes': {
                    'total': metrics.likes.total,
                    'successful': metrics.likes.successful,
                    'failed': metrics.likes.failed,
                },
                'comments': {
                    'total': metrics.comments.total,
                    'successful': metrics.comments.successful,
                    'failed': metrics.comments.failed,
                },
                'followers_history': list(metrics.followers_history),
                'following_history': list(metrics.following_history),
                'avg_engagement_rate': metrics.avg_engagement_rate,
                'start_time': metrics.start_time.isoformat(),
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to save metrics for {username}: {e}")
    
    async def _load_all_metrics(self):
        """Load all metrics from disk"""
        for username in self.account_metrics.keys():
            await self._load_metrics(username)
    
    async def _load_metrics(self, username: str):
        """Load metrics for an account"""
        metrics_file = self.metrics_dir / f"{username}_metrics.json"
        
        if not metrics_file.exists():
            return
        
        try:
            with open(metrics_file, 'r') as f:
                data = json.load(f)
            
            metrics = self.account_metrics[username]
            
            # Restore metrics
            metrics.follows = ActionMetrics(**data.get('follows', {}))
            metrics.likes = ActionMetrics(**data.get('likes', {}))
            metrics.comments = ActionMetrics(**data.get('comments', {}))
            
            metrics.followers_history = deque(
                data.get('followers_history', []),
                maxlen=1000
            )
            metrics.following_history = deque(
                data.get('following_history', []),
                maxlen=1000
            )
            
            metrics.avg_engagement_rate = data.get('avg_engagement_rate', 0.0)
            
            if 'start_time' in data:
                metrics.start_time = datetime.fromisoformat(data['start_time'])
            
            logger.info(f"Loaded metrics for {username}")
        
        except Exception as e:
            logger.warning(f"Failed to load metrics for {username}: {e}")
    
    def get_account_stats(self, username: str) -> Dict:
        """Get statistics for an account"""
        metrics = self.account_metrics.get(username)
        if not metrics:
            return {}
        
        # Calculate growth rates
        followers_growth = 0
        if len(metrics.followers_history) >= 2:
            recent = metrics.followers_history[-1]['count']
            old = metrics.followers_history[0]['count']
            followers_growth = recent - old
        
        # Calculate actions per hour
        uptime_hours = (datetime.now() - metrics.start_time).total_seconds() / 3600
        total_actions = (
            metrics.follows.total +
            metrics.likes.total +
            metrics.comments.total
        )
        actions_per_hour = total_actions / max(uptime_hours, 1)
        
        return {
            'username': username,
            'follows': {
                'total': metrics.follows.total,
                'success_rate': round(metrics.follows.success_rate, 4),
            },
            'likes': {
                'total': metrics.likes.total,
                'success_rate': round(metrics.likes.success_rate, 4),
            },
            'comments': {
                'total': metrics.comments.total,
                'success_rate': round(metrics.comments.success_rate, 4),
            },
            'followers': {
                'current': metrics.followers_history[-1]['count'] if metrics.followers_history else 0,
                'growth': followers_growth,
            },
            'following': {
                'current': metrics.following_history[-1]['count'] if metrics.following_history else 0,
            },
            'engagement_rate': round(metrics.avg_engagement_rate, 4),
            'actions_per_hour': round(actions_per_hour, 2),
            'uptime_hours': round(uptime_hours, 2),
        }
    
    def get_all_stats(self) -> List[Dict]:
        """Get statistics for all accounts"""
        return [self.get_account_stats(username) for username in self.account_metrics.keys()]
    
    def get_fleet_summary(self) -> Dict:
        """Get summary statistics for entire fleet"""
        total_actions = 0
        total_followers = 0
        total_accounts = len(self.account_metrics)
        active_accounts = 0
        
        for metrics in self.account_metrics.values():
            total_actions += (
                metrics.follows.total +
                metrics.likes.total +
                metrics.comments.total
            )
            
            if metrics.followers_history:
                total_followers += metrics.followers_history[-1]['count']
            
            # Check if active (activity in last hour)
            uptime = (datetime.now() - metrics.start_time).total_seconds()
            if uptime < 3600:
                active_accounts += 1
        
        return {
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'total_actions': total_actions,
            'total_followers': total_followers,
            'avg_followers_per_account': total_followers / max(total_accounts, 1),
        }
    
    async def shutdown(self):
        """Shutdown analytics system"""
        if self.tracking_task:
            self.tracking_task.cancel()
            try:
                await self.tracking_task
            except asyncio.CancelledError:
                pass
        
        # Save final metrics
        await self._save_all_metrics()
        
        logger.info("Analytics system shut down")


# Global analytics instance
analytics = Analytics()
