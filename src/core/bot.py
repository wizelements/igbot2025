"""
Core Instagram bot logic with intelligent automation
"""
import asyncio
import random
from typing import List, Optional, Dict, Any
from loguru import logger
from instagrapi import Client
from instagrapi.types import Media, User

from src.config import config
from src.services.multi_account_manager import account_manager
from src.services.scheduler import global_scheduler
from src.core.anti_ban import anti_ban_system
from src.core.analytics import analytics


class InstagramBot:
    """
    Core Instagram bot with intelligent automation
    """
    
    def __init__(self, username: str):
        self.username = username
        self.running = False
    
    async def start(self):
        """Start bot for this account"""
        logger.info(f"Starting bot for account {self.username}")
        self.running = True
        
        # Schedule all jobs
        await self._schedule_jobs()
        
        logger.success(f"Bot started for {self.username}")
    
    async def stop(self):
        """Stop bot"""
        logger.info(f"Stopping bot for {self.username}")
        self.running = False
    
    async def _schedule_jobs(self):
        """Schedule all automation jobs"""
        # Follow job
        global_scheduler.schedule_follow_job(
            self.username,
            lambda: asyncio.create_task(self.auto_follow())
        )
        
        # Like job
        global_scheduler.schedule_like_job(
            self.username,
            lambda: asyncio.create_task(self.auto_like())
        )
        
        # Comment job
        global_scheduler.schedule_comment_job(
            self.username,
            lambda: asyncio.create_task(self.auto_comment())
        )
        
        # Unfollow job
        global_scheduler.schedule_unfollow_job(
            self.username,
            lambda: asyncio.create_task(self.auto_unfollow())
        )
        
        # Daily reset
        global_scheduler.schedule_daily_reset(self.username)
    
    async def auto_follow(self):
        """Automatically follow targeted users"""
        if not self.running:
            return
        
        try:
            # Get scheduler for this account
            acc_scheduler = global_scheduler.account_schedulers.get(self.username)
            if not acc_scheduler:
                return
            
            # Check if we can perform follow action
            if not acc_scheduler.can_perform_action('follow'):
                logger.debug(f"[{self.username}] Daily follow limit reached")
                return
            
            # Apply anti-ban delay
            await anti_ban_system.apply_human_delay(self.username)
            
            # Get target users
            targets = await self._get_follow_targets()
            if not targets:
                return
            
            # Follow a random target
            target = random.choice(targets)
            
            async def follow_action(client: Client):
                client.user_follow(target.pk)
                return target
            
            result = await account_manager.perform_action(
                self.username,
                'follow',
                follow_action
            )
            
            if result:
                acc_scheduler.increment_action('follow')
                await analytics.track_action(self.username, 'follow', success=True)
                logger.success(f"[{self.username}] Followed @{target.username}")
            
        except Exception as e:
            logger.error(f"[{self.username}] Auto-follow error: {e}")
            await analytics.track_action(self.username, 'follow', success=False)
    
    async def auto_like(self):
        """Automatically like posts"""
        if not self.running:
            return
        
        try:
            acc_scheduler = global_scheduler.account_schedulers.get(self.username)
            if not acc_scheduler or not acc_scheduler.can_perform_action('like'):
                return
            
            await anti_ban_system.apply_human_delay(self.username)
            
            # Get media to like
            media_list = await self._get_like_targets()
            if not media_list:
                return
            
            media = random.choice(media_list)
            
            async def like_action(client: Client):
                client.media_like(media.pk)
                return media
            
            result = await account_manager.perform_action(
                self.username,
                'like',
                like_action
            )
            
            if result:
                acc_scheduler.increment_action('like')
                await analytics.track_action(self.username, 'like', success=True)
                logger.success(f"[{self.username}] Liked post {media.pk}")
        
        except Exception as e:
            logger.error(f"[{self.username}] Auto-like error: {e}")
            await analytics.track_action(self.username, 'like', success=False)
    
    async def auto_comment(self):
        """Automatically comment on posts"""
        if not self.running:
            return
        
        try:
            acc_scheduler = global_scheduler.account_schedulers.get(self.username)
            if not acc_scheduler or not acc_scheduler.can_perform_action('comment'):
                return
            
            await anti_ban_system.apply_human_delay(self.username, action_type='comment')
            
            # Get media to comment on
            media_list = await self._get_comment_targets()
            if not media_list:
                return
            
            media = random.choice(media_list)
            comment_text = self._generate_comment()
            
            async def comment_action(client: Client):
                client.media_comment(media.pk, comment_text)
                return media
            
            result = await account_manager.perform_action(
                self.username,
                'comment',
                comment_action
            )
            
            if result:
                acc_scheduler.increment_action('comment')
                await analytics.track_action(self.username, 'comment', success=True)
                logger.success(f"[{self.username}] Commented on post {media.pk}: {comment_text}")
        
        except Exception as e:
            logger.error(f"[{self.username}] Auto-comment error: {e}")
            await analytics.track_action(self.username, 'comment', success=False)
    
    async def auto_unfollow(self):
        """Automatically unfollow old follows"""
        if not self.running:
            return
        
        try:
            logger.info(f"[{self.username}] Running cleanup unfollow")
            
            client = await account_manager.get_client(self.username)
            if not client:
                return
            
            # Get followings
            async def get_followings(c: Client):
                return c.user_following(c.user_id)
            
            followings = await asyncio.to_thread(get_followings, client)
            
            # Unfollow non-followers (keep ratio healthy)
            unfollow_count = 0
            max_unfollows = 50  # Per run
            
            for user_id, user in list(followings.items())[:100]:
                if unfollow_count >= max_unfollows:
                    break
                
                # Check if they follow back
                async def check_follower(c: Client):
                    followers = c.user_followers(c.user_id, amount=1000)
                    return user_id in followers
                
                is_follower = await asyncio.to_thread(check_follower, client)
                
                if not is_follower:
                    # Unfollow
                    async def unfollow_action(c: Client):
                        c.user_unfollow(user_id)
                    
                    await account_manager.perform_action(
                        self.username,
                        'unfollow',
                        unfollow_action
                    )
                    
                    unfollow_count += 1
                    await asyncio.sleep(random.uniform(2, 5))
            
            logger.success(f"[{self.username}] Unfollowed {unfollow_count} non-followers")
        
        except Exception as e:
            logger.error(f"[{self.username}] Auto-unfollow error: {e}")
    
    async def _get_follow_targets(self) -> List[User]:
        """Get targeted users to follow"""
        client = await account_manager.get_client(self.username)
        if not client:
            return []
        
        try:
            # Get users from explore/hashtags
            async def get_explore_users(c: Client):
                users = []
                # Get from hashtag
                hashtags = ['motivation', 'entrepreneur', 'fitness', 'lifestyle']
                tag = random.choice(hashtags)
                
                medias = c.hashtag_medias_recent(tag, amount=20)
                for media in medias:
                    users.append(media.user)
                
                return users
            
            users = await asyncio.to_thread(get_explore_users, client)
            return users[:10]
        
        except Exception as e:
            logger.error(f"Error getting follow targets: {e}")
            return []
    
    async def _get_like_targets(self) -> List[Media]:
        """Get media to like"""
        client = await account_manager.get_client(self.username)
        if not client:
            return []
        
        try:
            async def get_timeline(c: Client):
                return c.get_timeline_feed()
            
            feed = await asyncio.to_thread(get_timeline, client)
            return feed[:20] if feed else []
        
        except Exception as e:
            logger.error(f"Error getting like targets: {e}")
            return []
    
    async def _get_comment_targets(self) -> List[Media]:
        """Get media to comment on"""
        return await self._get_like_targets()
    
    def _generate_comment(self) -> str:
        """Generate human-like comment"""
        comments = [
            "Great content! 🔥",
            "Love this! ❤️",
            "Amazing! 😍",
            "So inspiring! ✨",
            "This is awesome! 💯",
            "Keep it up! 👏",
            "Incredible! 🙌",
            "Beautiful! 💖",
            "Perfect! ⭐",
            "Stunning! 🌟",
        ]
        return random.choice(comments)


class BotFleet:
    """
    Manager for all bot instances
    """
    
    def __init__(self):
        self.bots: Dict[str, InstagramBot] = {}
    
    async def initialize(self):
        """Initialize all bots"""
        logger.info("Initializing bot fleet")
        
        for account in config.IG_ACCOUNTS:
            username = account['username']
            bot = InstagramBot(username)
            self.bots[username] = bot
        
        logger.success(f"Bot fleet initialized with {len(self.bots)} bots")
    
    async def start_all(self):
        """Start all bots"""
        logger.info("Starting all bots")
        
        tasks = [bot.start() for bot in self.bots.values()]
        await asyncio.gather(*tasks)
        
        logger.success("All bots started")
    
    async def stop_all(self):
        """Stop all bots"""
        logger.info("Stopping all bots")
        
        tasks = [bot.stop() for bot in self.bots.values()]
        await asyncio.gather(*tasks)
        
        logger.success("All bots stopped")
    
    def get_bot(self, username: str) -> Optional[InstagramBot]:
        """Get specific bot"""
        return self.bots.get(username)


# Global bot fleet
bot_fleet = BotFleet()
