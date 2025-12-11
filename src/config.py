"""
Central configuration management for igbot2025
"""
import os
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
import pytz

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class ProxyConfig(BaseModel):
    pool_size: int = Field(default=100, ge=1)
    rotation_interval: int = Field(default=300, ge=30)
    providers: List[str] = Field(default_factory=list)
    api_key: str = ""
    username: str = ""
    password: str = ""
    health_check_interval: int = Field(default=60, ge=10)
    max_latency_ms: int = Field(default=3000, ge=100)
    blacklist_threshold: int = Field(default=5, ge=1)


class AntiBanConfig(BaseModel):
    enable_human_simulation: bool = True
    warmup_period_days: int = Field(default=14, ge=1)
    max_follows_per_day: int = Field(default=200, ge=1)
    max_likes_per_day: int = Field(default=500, ge=1)
    max_comments_per_day: int = Field(default=50, ge=1)
    max_unfollows_per_day: int = Field(default=200, ge=1)
    min_delay_seconds: int = Field(default=30, ge=10)
    max_delay_seconds: int = Field(default=180, ge=30)
    shadowban_detection: bool = True
    action_variance: float = Field(default=0.3, ge=0.0, le=1.0)


class SchedulerConfig(BaseModel):
    timezone: str = "America/Los_Angeles"
    peak_hours_start: int = Field(default=10, ge=0, le=23)
    peak_hours_end: int = Field(default=21, ge=0, le=23)
    actions_per_hour_min: int = Field(default=30, ge=1)
    actions_per_hour_max: int = Field(default=60, ge=1)
    weekend_multiplier: float = Field(default=1.2, ge=0.5, le=2.0)

    @validator('timezone')
    def validate_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v


class DashboardConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    secret_key: str = "change-me-in-production"
    username: str = "admin"
    password: str = "change-this-password"
    enable_auth: bool = True
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///igbot2025.db"
    mongodb_url: str = "mongodb://localhost:27017/igbot2025"
    redis_url: str = "redis://localhost:6379/0"
    pool_size: int = Field(default=20, ge=1)
    max_overflow: int = Field(default=10, ge=0)


class ContentConfig(BaseModel):
    auto_remix_reels: bool = True
    fyp_optimization: bool = True
    hashtag_research: bool = True
    openai_api_key: str = ""
    max_hashtags: int = Field(default=30, ge=1, le=30)
    min_engagement_rate: float = Field(default=0.02, ge=0.0, le=1.0)


class MonitoringConfig(BaseModel):
    prometheus_port: int = Field(default=9090, ge=1, le=65535)
    enable_metrics: bool = True
    sentry_dsn: str = ""
    log_level: str = "INFO"
    log_file: str = "logs/igbot2025.log"


class EmergencyConfig(BaseModel):
    kill_switch_enabled: bool = False
    auto_pause_on_anomaly: bool = True
    max_ban_risk_score: int = Field(default=75, ge=0, le=100)
    min_success_rate: float = Field(default=0.8, ge=0.0, le=1.0)
    alert_email: str = ""
    alert_webhook: str = ""


class Config:
    """Main configuration class"""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT != "production"
    
    # Instagram Accounts
    IG_ACCOUNTS: List[Dict[str, str]] = []
    
    # Sub-configs
    proxy: ProxyConfig
    anti_ban: AntiBanConfig
    scheduler: SchedulerConfig
    dashboard: DashboardConfig
    database: DatabaseConfig
    content: ContentConfig
    monitoring: MonitoringConfig
    emergency: EmergencyConfig
    
    # Deployment
    DEPLOY_REGION: str = os.getenv("DEPLOY_REGION", "us-west-2")
    SCALE_REPLICAS: int = int(os.getenv("SCALE_REPLICAS", "1"))
    
    def __init__(self):
        self._load_accounts()
        self._load_configs()
    
    def _load_accounts(self):
        """Parse Instagram accounts from environment"""
        accounts_str = os.getenv("IG_ACCOUNTS", "")
        if accounts_str:
            for acc in accounts_str.split(","):
                parts = acc.strip().split(":")
                if len(parts) >= 2:
                    account = {
                        "username": parts[0],
                        "password": parts[1],
                        "2fa_secret": parts[2] if len(parts) > 2 else ""
                    }
                    self.IG_ACCOUNTS.append(account)
    
    def _load_configs(self):
        """Initialize all sub-configurations"""
        self.proxy = ProxyConfig(
            pool_size=int(os.getenv("PROXY_POOL_SIZE", "100")),
            rotation_interval=int(os.getenv("PROXY_ROTATION_INTERVAL", "300")),
            providers=os.getenv("PROXY_PROVIDERS", "").split(",") if os.getenv("PROXY_PROVIDERS") else [],
            api_key=os.getenv("PROXY_API_KEY", ""),
            username=os.getenv("PROXY_USERNAME", ""),
            password=os.getenv("PROXY_PASSWORD", "")
        )
        
        self.anti_ban = AntiBanConfig(
            enable_human_simulation=os.getenv("ENABLE_HUMAN_SIMULATION", "true").lower() == "true",
            warmup_period_days=int(os.getenv("WARMUP_PERIOD_DAYS", "14")),
            max_follows_per_day=int(os.getenv("MAX_FOLLOWS_PER_DAY", "200")),
            max_likes_per_day=int(os.getenv("MAX_LIKES_PER_DAY", "500")),
            max_comments_per_day=int(os.getenv("MAX_COMMENTS_PER_DAY", "50")),
            shadowban_detection=os.getenv("SHADOWBAN_DETECTION", "true").lower() == "true"
        )
        
        self.scheduler = SchedulerConfig(
            timezone=os.getenv("TIMEZONE", "America/Los_Angeles"),
            peak_hours_start=int(os.getenv("PEAK_HOURS_START", "10")),
            peak_hours_end=int(os.getenv("PEAK_HOURS_END", "21")),
            actions_per_hour_min=int(os.getenv("ACTIONS_PER_HOUR_MIN", "30")),
            actions_per_hour_max=int(os.getenv("ACTIONS_PER_HOUR_MAX", "60"))
        )
        
        self.dashboard = DashboardConfig(
            host=os.getenv("DASHBOARD_HOST", "0.0.0.0"),
            port=int(os.getenv("DASHBOARD_PORT", "8000")),
            secret_key=os.getenv("DASHBOARD_SECRET_KEY", "change-me-in-production"),
            username=os.getenv("DASHBOARD_USERNAME", "admin"),
            password=os.getenv("DASHBOARD_PASSWORD", "change-this-password")
        )
        
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///igbot2025.db"),
            mongodb_url=os.getenv("MONGODB_URL", "mongodb://localhost:27017/igbot2025"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
        )
        
        self.content = ContentConfig(
            auto_remix_reels=os.getenv("AUTO_REMIX_REELS", "true").lower() == "true",
            fyp_optimization=os.getenv("FYP_OPTIMIZATION", "true").lower() == "true",
            hashtag_research=os.getenv("HASHTAG_RESEARCH", "true").lower() == "true",
            openai_api_key=os.getenv("OPENAI_API_KEY", "")
        )
        
        self.monitoring = MonitoringConfig(
            prometheus_port=int(os.getenv("PROMETHEUS_PORT", "9090")),
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            sentry_dsn=os.getenv("SENTRY_DSN", ""),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
        
        self.emergency = EmergencyConfig(
            kill_switch_enabled=os.getenv("KILL_SWITCH_ENABLED", "false").lower() == "true",
            auto_pause_on_anomaly=os.getenv("AUTO_PAUSE_ON_ANOMALY", "true").lower() == "true",
            max_ban_risk_score=int(os.getenv("MAX_BAN_RISK_SCORE", "75"))
        )


# Global config instance
config = Config()
