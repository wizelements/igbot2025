"""
Advanced APScheduler with per-account cron jobs, peak-hour detection, and timezone-aware scheduling
"""
import asyncio
from datetime import datetime, time as dt_time
from typing import Dict, List, Callable, Optional
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.redis import RedisJobStore
from loguru import logger
import random

from src.config import config


class AccountScheduler:
    """
    Per-account scheduler with intelligent timing
    """
    
    def __init__(self, username: str):
        self.username = username
        self.timezone = pytz.timezone(config.scheduler.timezone)
        self.jobs: Dict[str, str] = {}  # job_name -> job_id
        self.action_counts: Dict[str, int] = {
            'follow': 0,
            'like': 0,
            'comment': 0,
            'unfollow': 0,
            'post': 0
        }
        self.daily_reset_time: Optional[datetime] = None
    
    def is_peak_hours(self) -> bool:
        """Check if current time is within peak hours"""
        now = datetime.now(self.timezone)
        current_hour = now.hour
        
        # Check weekend multiplier
        is_weekend = now.weekday() >= 5
        
        # Adjust peak hours for weekend
        if is_weekend:
            # Extend peak hours on weekends
            start = max(0, config.scheduler.peak_hours_start - 2)
            end = min(23, config.scheduler.peak_hours_end + 2)
        else:
            start = config.scheduler.peak_hours_start
            end = config.scheduler.peak_hours_end
        
        return start <= current_hour <= end
    
    def get_actions_per_hour(self) -> int:
        """Get dynamic actions per hour based on time"""
        base_min = config.scheduler.actions_per_hour_min
        base_max = config.scheduler.actions_per_hour_max
        
        if self.is_peak_hours():
            # Increase activity during peak hours
            multiplier = 1.5
        else:
            # Reduce activity during off-peak
            multiplier = 0.7
        
        # Weekend boost
        now = datetime.now(self.timezone)
        if now.weekday() >= 5:
            multiplier *= config.scheduler.weekend_multiplier
        
        min_actions = int(base_min * multiplier)
        max_actions = int(base_max * multiplier)
        
        return random.randint(min_actions, max_actions)
    
    def get_next_action_delay(self) -> int:
        """Calculate next action delay in seconds (human-like variance)"""
        actions_per_hour = self.get_actions_per_hour()
        base_delay = 3600 / actions_per_hour
        
        # Add human variance (±30%)
        variance = random.uniform(-0.3, 0.3)
        delay = base_delay * (1 + variance)
        
        # Ensure within bounds
        return max(config.anti_ban.min_delay_seconds, 
                  min(int(delay), config.anti_ban.max_delay_seconds))
    
    def reset_daily_counts(self):
        """Reset daily action counts"""
        self.action_counts = {k: 0 for k in self.action_counts}
        logger.info(f"[{self.username}] Daily action counts reset")
    
    def can_perform_action(self, action_type: str) -> bool:
        """Check if action can be performed based on daily limits"""
        limits = {
            'follow': config.anti_ban.max_follows_per_day,
            'like': config.anti_ban.max_likes_per_day,
            'comment': config.anti_ban.max_comments_per_day,
            'unfollow': config.anti_ban.max_unfollows_per_day,
        }
        
        if action_type not in limits:
            return True
        
        return self.action_counts.get(action_type, 0) < limits[action_type]
    
    def increment_action(self, action_type: str):
        """Increment action counter"""
        self.action_counts[action_type] = self.action_counts.get(action_type, 0) + 1


class GlobalScheduler:
    """
    Global scheduler managing all accounts with APScheduler
    """
    
    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.account_schedulers: Dict[str, AccountScheduler] = {}
        self.running = False
    
    async def initialize(self):
        """Initialize the scheduler"""
        logger.info("Initializing global scheduler")
        
        # Configure job store (Redis for distributed systems)
        jobstores = {}
        if config.database.redis_url:
            try:
                jobstores['default'] = RedisJobStore(
                    host=config.database.redis_url.split('//')[1].split(':')[0],
                    port=int(config.database.redis_url.split(':')[-1].split('/')[0]),
                    db=0
                )
            except Exception as e:
                logger.warning(f"Could not connect to Redis for job store: {e}")
        
        # Create scheduler
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            timezone=config.scheduler.timezone
        )
        
        # Create per-account schedulers
        for account in config.IG_ACCOUNTS:
            username = account['username']
            self.account_schedulers[username] = AccountScheduler(username)
        
        # Start scheduler
        self.scheduler.start()
        self.running = True
        
        logger.success(f"Global scheduler initialized with {len(self.account_schedulers)} accounts")
    
    def schedule_account_job(
        self,
        username: str,
        job_name: str,
        func: Callable,
        trigger_type: str = "interval",
        **trigger_kwargs
    ) -> str:
        """
        Schedule a job for a specific account
        
        Args:
            username: Account username
            job_name: Name of the job
            func: Function to execute
            trigger_type: "interval", "cron", or "date"
            **trigger_kwargs: Trigger-specific arguments
        """
        if username not in self.account_schedulers:
            raise ValueError(f"Account {username} not found")
        
        acc_scheduler = self.account_schedulers[username]
        
        # Create trigger
        if trigger_type == "interval":
            trigger = IntervalTrigger(**trigger_kwargs)
        elif trigger_type == "cron":
            trigger = CronTrigger(timezone=acc_scheduler.timezone, **trigger_kwargs)
        elif trigger_type == "date":
            trigger = DateTrigger(**trigger_kwargs)
        else:
            raise ValueError(f"Unknown trigger type: {trigger_type}")
        
        # Add job
        job = self.scheduler.add_job(
            func,
            trigger=trigger,
            id=f"{username}_{job_name}",
            name=f"[{username}] {job_name}",
            replace_existing=True
        )
        
        acc_scheduler.jobs[job_name] = job.id
        
        logger.info(f"Scheduled job '{job_name}' for account {username}")
        return job.id
    
    def schedule_peak_hours_job(
        self,
        username: str,
        job_name: str,
        func: Callable,
        **kwargs
    ):
        """
        Schedule job to run only during peak hours
        """
        acc_scheduler = self.account_schedulers[username]
        
        # Create cron for peak hours
        self.schedule_account_job(
            username=username,
            job_name=job_name,
            func=func,
            trigger_type="cron",
            hour=f"{config.scheduler.peak_hours_start}-{config.scheduler.peak_hours_end}",
            **kwargs
        )
    
    def schedule_daily_reset(self, username: str):
        """Schedule daily counter reset at midnight"""
        acc_scheduler = self.account_schedulers[username]
        
        self.schedule_account_job(
            username=username,
            job_name="daily_reset",
            func=acc_scheduler.reset_daily_counts,
            trigger_type="cron",
            hour=0,
            minute=0
        )
    
    def schedule_follow_job(self, username: str, target_func: Callable):
        """Schedule intelligent follow job"""
        self.schedule_account_job(
            username=username,
            job_name="auto_follow",
            func=target_func,
            trigger_type="interval",
            seconds=300,  # Every 5 minutes, but with delay logic
        )
    
    def schedule_like_job(self, username: str, target_func: Callable):
        """Schedule intelligent like job"""
        self.schedule_account_job(
            username=username,
            job_name="auto_like",
            func=target_func,
            trigger_type="interval",
            seconds=180,  # Every 3 minutes
        )
    
    def schedule_comment_job(self, username: str, target_func: Callable):
        """Schedule intelligent comment job"""
        # Comments are more sensitive, schedule less frequently
        self.schedule_account_job(
            username=username,
            job_name="auto_comment",
            func=target_func,
            trigger_type="interval",
            seconds=600,  # Every 10 minutes
        )
    
    def schedule_unfollow_job(self, username: str, target_func: Callable):
        """Schedule unfollow job (cleanup old follows)"""
        self.schedule_account_job(
            username=username,
            job_name="auto_unfollow",
            func=target_func,
            trigger_type="cron",
            hour=3,  # 3 AM when activity is low
            minute=0
        )
    
    def schedule_content_post(self, username: str, target_func: Callable):
        """Schedule content posting during optimal times"""
        acc_scheduler = self.account_schedulers[username]
        
        # Post during peak engagement hours
        optimal_hours = [9, 12, 15, 18, 21]  # Peak engagement times
        
        for hour in optimal_hours:
            self.schedule_account_job(
                username=username,
                job_name=f"post_{hour}h",
                func=target_func,
                trigger_type="cron",
                hour=hour,
                minute=random.randint(0, 59),  # Random minute
            )
    
    def pause_account(self, username: str):
        """Pause all jobs for an account"""
        if username not in self.account_schedulers:
            return
        
        acc_scheduler = self.account_schedulers[username]
        
        for job_id in acc_scheduler.jobs.values():
            self.scheduler.pause_job(job_id)
        
        logger.warning(f"Paused all jobs for account {username}")
    
    def resume_account(self, username: str):
        """Resume all jobs for an account"""
        if username not in self.account_schedulers:
            return
        
        acc_scheduler = self.account_schedulers[username]
        
        for job_id in acc_scheduler.jobs.values():
            self.scheduler.resume_job(job_id)
        
        logger.info(f"Resumed all jobs for account {username}")
    
    def remove_account_job(self, username: str, job_name: str):
        """Remove a specific job"""
        if username not in self.account_schedulers:
            return
        
        acc_scheduler = self.account_schedulers[username]
        
        if job_name in acc_scheduler.jobs:
            job_id = acc_scheduler.jobs[job_name]
            self.scheduler.remove_job(job_id)
            del acc_scheduler.jobs[job_name]
            logger.info(f"Removed job '{job_name}' for account {username}")
    
    def get_account_stats(self, username: str) -> Dict:
        """Get statistics for an account"""
        if username not in self.account_schedulers:
            return {}
        
        acc_scheduler = self.account_schedulers[username]
        
        return {
            'username': username,
            'timezone': str(acc_scheduler.timezone),
            'is_peak_hours': acc_scheduler.is_peak_hours(),
            'actions_per_hour': acc_scheduler.get_actions_per_hour(),
            'next_action_delay': acc_scheduler.get_next_action_delay(),
            'daily_actions': acc_scheduler.action_counts,
            'active_jobs': len(acc_scheduler.jobs),
            'job_names': list(acc_scheduler.jobs.keys())
        }
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        return jobs
    
    async def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler:
            self.scheduler.shutdown()
        self.running = False
        logger.info("Global scheduler shut down")


# Global scheduler instance
global_scheduler = GlobalScheduler()
