"""
Advanced proxy rotation system with health checking and auto-blacklisting
"""
import asyncio
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
from loguru import logger
import random
from collections import defaultdict

from src.config import config


class ProxyType(Enum):
    RESIDENTIAL = "residential"
    MOBILE = "mobile"
    DATACENTER = "datacenter"


class ProxyProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


@dataclass
class Proxy:
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: ProxyType = ProxyType.DATACENTER
    protocol: ProxyProtocol = ProxyProtocol.HTTP
    
    # Health metrics
    latency_ms: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    last_check: float = field(default_factory=time.time)
    last_rotation: float = field(default_factory=time.time)
    blacklisted: bool = False
    blacklist_until: float = 0.0
    
    @property
    def url(self) -> str:
        """Get formatted proxy URL"""
        auth = ""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        return f"{self.protocol.value}://{auth}{self.host}:{self.port}"
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 1.0
        return self.success_count / total
    
    @property
    def is_healthy(self) -> bool:
        """Check if proxy is healthy"""
        if self.blacklisted and time.time() < self.blacklist_until:
            return False
        if self.failure_count >= config.proxy.blacklist_threshold:
            return False
        return self.success_rate >= 0.7


class ProxyRotator:
    """
    Advanced proxy rotation with health checking, auto-blacklisting,
    and support for residential/mobile/datacenter pools
    """
    
    def __init__(self):
        self.proxies: List[Proxy] = []
        self.proxy_index: int = 0
        self.account_proxies: Dict[str, Proxy] = {}
        self.health_check_task: Optional[asyncio.Task] = None
        self.stats: Dict[str, any] = defaultdict(int)
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        """Initialize proxy pool"""
        logger.info(f"Initializing proxy rotator with {config.proxy.pool_size} proxies")
        
        # Load proxies from providers
        await self._load_proxies()
        
        # Start health check loop
        self.health_check_task = asyncio.create_task(self._health_check_loop())
        
        logger.success(f"Proxy rotator initialized with {len(self.proxies)} proxies")
    
    async def _load_proxies(self):
        """Load proxies from configured providers"""
        # Example proxy generation (in production, fetch from API)
        for i in range(config.proxy.pool_size):
            proxy_type = random.choice(list(ProxyType))
            protocol = ProxyProtocol.SOCKS5 if random.random() > 0.5 else ProxyProtocol.HTTP
            
            proxy = Proxy(
                host=f"proxy{i}.example.com",
                port=random.choice([8080, 3128, 1080, 9050]),
                username=config.proxy.username,
                password=config.proxy.password,
                proxy_type=proxy_type,
                protocol=protocol
            )
            self.proxies.append(proxy)
        
        # Shuffle for randomness
        random.shuffle(self.proxies)
    
    async def get_proxy(self, account_username: Optional[str] = None, 
                       prefer_type: Optional[ProxyType] = None) -> Optional[Proxy]:
        """
        Get a healthy proxy for an account
        
        Args:
            account_username: Pin proxy to specific account for session consistency
            prefer_type: Prefer specific proxy type (residential/mobile/datacenter)
        """
        async with self._lock:
            # Return pinned proxy for account if available
            if account_username and account_username in self.account_proxies:
                proxy = self.account_proxies[account_username]
                if proxy.is_healthy:
                    return proxy
                else:
                    # Remove unhealthy pinned proxy
                    del self.account_proxies[account_username]
            
            # Find healthy proxy
            healthy_proxies = [p for p in self.proxies if p.is_healthy]
            
            if not healthy_proxies:
                logger.error("No healthy proxies available!")
                return None
            
            # Filter by preferred type
            if prefer_type:
                typed_proxies = [p for p in healthy_proxies if p.proxy_type == prefer_type]
                if typed_proxies:
                    healthy_proxies = typed_proxies
            
            # Rotate through proxies
            proxy = healthy_proxies[self.proxy_index % len(healthy_proxies)]
            self.proxy_index += 1
            
            # Pin to account
            if account_username:
                self.account_proxies[account_username] = proxy
            
            proxy.last_rotation = time.time()
            self.stats['rotations'] += 1
            
            logger.debug(f"Assigned {proxy.proxy_type.value} proxy {proxy.host}:{proxy.port} "
                        f"(latency: {proxy.latency_ms:.0f}ms, success rate: {proxy.success_rate:.2%})")
            
            return proxy
    
    async def _health_check_loop(self):
        """Continuous health checking of all proxies"""
        logger.info("Starting proxy health check loop")
        
        while True:
            try:
                await asyncio.sleep(config.proxy.health_check_interval)
                
                logger.debug(f"Running health checks on {len(self.proxies)} proxies")
                
                # Check all proxies concurrently
                tasks = [self._check_proxy_health(proxy) for proxy in self.proxies]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                healthy = sum(1 for r in results if r is True)
                unhealthy = len(results) - healthy
                
                logger.info(f"Health check complete: {healthy} healthy, {unhealthy} unhealthy")
                
                # Update stats
                self.stats['last_health_check'] = time.time()
                self.stats['healthy_proxies'] = healthy
                self.stats['unhealthy_proxies'] = unhealthy
                
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
    
    async def _check_proxy_health(self, proxy: Proxy) -> bool:
        """
        Check individual proxy health
        
        Tests:
        1. Latency check
        2. Instagram reachability
        3. Response validity
        """
        start_time = time.time()
        
        try:
            # Test both generic endpoint and Instagram
            test_urls = [
                "https://httpbin.org/ip",
                "https://www.instagram.com/",
            ]
            
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                for url in test_urls:
                    async with session.get(
                        url,
                        proxy=proxy.url if proxy.protocol != ProxyProtocol.SOCKS5 else None
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"Bad status: {response.status}")
                        
                        # Check Instagram specifically
                        if "instagram.com" in url:
                            text = await response.text()
                            if "instagram" not in text.lower():
                                raise Exception("Instagram unreachable")
            
            # Calculate latency
            latency = (time.time() - start_time) * 1000
            proxy.latency_ms = latency
            
            # Check latency threshold
            if latency > config.proxy.max_latency_ms:
                logger.warning(f"Proxy {proxy.host}:{proxy.port} has high latency: {latency:.0f}ms")
                proxy.failure_count += 1
                return False
            
            # Success
            proxy.success_count += 1
            proxy.last_check = time.time()
            
            # Reset blacklist if recovered
            if proxy.blacklisted and proxy.success_rate > 0.8:
                proxy.blacklisted = False
                logger.info(f"Proxy {proxy.host}:{proxy.port} recovered from blacklist")
            
            return True
            
        except Exception as e:
            proxy.failure_count += 1
            proxy.last_check = time.time()
            
            logger.debug(f"Proxy {proxy.host}:{proxy.port} health check failed: {e}")
            
            # Auto-blacklist if too many failures
            if proxy.failure_count >= config.proxy.blacklist_threshold:
                proxy.blacklisted = True
                proxy.blacklist_until = time.time() + 3600  # 1 hour
                logger.warning(f"Proxy {proxy.host}:{proxy.port} blacklisted for 1 hour")
            
            return False
    
    async def report_proxy_result(self, proxy: Proxy, success: bool):
        """Report result of using a proxy"""
        async with self._lock:
            if success:
                proxy.success_count += 1
                self.stats['successful_requests'] += 1
            else:
                proxy.failure_count += 1
                self.stats['failed_requests'] += 1
                
                # Blacklist if threshold exceeded
                if proxy.failure_count >= config.proxy.blacklist_threshold:
                    proxy.blacklisted = True
                    proxy.blacklist_until = time.time() + 3600
                    logger.warning(f"Proxy {proxy.host}:{proxy.port} auto-blacklisted")
    
    def get_stats(self) -> Dict:
        """Get proxy rotator statistics"""
        healthy = sum(1 for p in self.proxies if p.is_healthy)
        blacklisted = sum(1 for p in self.proxies if p.blacklisted)
        
        avg_latency = sum(p.latency_ms for p in self.proxies if p.is_healthy) / max(healthy, 1)
        avg_success_rate = sum(p.success_rate for p in self.proxies) / len(self.proxies)
        
        return {
            'total_proxies': len(self.proxies),
            'healthy_proxies': healthy,
            'blacklisted_proxies': blacklisted,
            'average_latency_ms': round(avg_latency, 2),
            'average_success_rate': round(avg_success_rate, 4),
            'total_rotations': self.stats['rotations'],
            'successful_requests': self.stats['successful_requests'],
            'failed_requests': self.stats['failed_requests'],
            'accounts_with_proxies': len(self.account_proxies)
        }
    
    async def shutdown(self):
        """Shutdown proxy rotator"""
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        logger.info("Proxy rotator shut down")


# Global proxy rotator instance
proxy_rotator = ProxyRotator()
