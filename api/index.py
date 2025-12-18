"""
Vercel serverless function entry point for igbot2025
FastAPI application for Instagram bot management
"""
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import secrets
from datetime import datetime

# Initialize FastAPI
app = FastAPI(
    title="IGBot 2025",
    description="Instagram Bot Management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic auth credentials"""
    correct_username = secrets.compare_digest(
        credentials.username, 
        os.getenv("DASHBOARD_USERNAME", "admin")
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        os.getenv("DASHBOARD_PASSWORD", "changeme")
    )
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str


class AccountStatus(BaseModel):
    username: str
    status: str
    is_active: bool
    last_action: Optional[str]
    actions_today: Dict[str, int]


class BotCommand(BaseModel):
    action: str
    username: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class AccountAdd(BaseModel):
    username: str
    password: str
    two_fa_secret: Optional[str] = None


# In-memory state (for demo - use database in production)
bot_state = {
    "active_accounts": [],
    "total_actions": 0,
    "started_at": datetime.utcnow().isoformat()
}


# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "IGBot 2025 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "production")
    )


@app.get("/debug/env")
async def debug_env():
    """Debug endpoint to check env vars (remove in production)"""
    return {
        "has_username": bool(os.getenv("DASHBOARD_USERNAME")),
        "has_password": bool(os.getenv("DASHBOARD_PASSWORD")),
        "username_len": len(os.getenv("DASHBOARD_USERNAME", "")),
        "password_len": len(os.getenv("DASHBOARD_PASSWORD", "")),
    }


@app.get("/api/status")
async def get_status(username: str = Depends(verify_credentials)):
    """Get bot fleet status"""
    return {
        "status": "running",
        "accounts": len(bot_state["active_accounts"]),
        "total_actions": bot_state["total_actions"],
        "uptime": bot_state["started_at"],
        "active_accounts": bot_state["active_accounts"]
    }


@app.get("/api/accounts", response_model=List[AccountStatus])
async def list_accounts(username: str = Depends(verify_credentials)):
    """List all Instagram accounts"""
    accounts = []
    
    # Parse accounts from environment
    accounts_str = os.getenv("IG_ACCOUNTS", "")
    if accounts_str:
        for acc in accounts_str.split(","):
            parts = acc.strip().split(":")
            if len(parts) >= 2:
                accounts.append(AccountStatus(
                    username=parts[0],
                    status="active",
                    is_active=parts[0] in bot_state["active_accounts"],
                    last_action=None,
                    actions_today={
                        "follow": 0,
                        "like": 0,
                        "comment": 0,
                        "unfollow": 0
                    }
                ))
    
    return accounts


@app.post("/api/accounts/add")
async def add_account(
    account: AccountAdd,
    username: str = Depends(verify_credentials)
):
    """Add new Instagram account"""
    # In production, this would add to database
    return {
        "status": "success",
        "message": f"Account {account.username} added successfully",
        "username": account.username
    }


@app.post("/api/bot/start")
async def start_bot(
    background_tasks: BackgroundTasks,
    username: str = Depends(verify_credentials)
):
    """Start the bot for all accounts or specific account"""
    
    async def start_bot_background():
        # Parse accounts from environment
        accounts_str = os.getenv("IG_ACCOUNTS", "")
        if accounts_str:
            for acc in accounts_str.split(","):
                parts = acc.strip().split(":")
                if len(parts) >= 2 and parts[0] not in bot_state["active_accounts"]:
                    bot_state["active_accounts"].append(parts[0])
    
    background_tasks.add_task(start_bot_background)
    
    return {
        "status": "success",
        "message": "Bot started successfully",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/bot/stop")
async def stop_bot(username: str = Depends(verify_credentials)):
    """Stop the bot"""
    bot_state["active_accounts"] = []
    
    return {
        "status": "success",
        "message": "Bot stopped successfully",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/bot/command")
async def execute_command(
    command: BotCommand,
    username: str = Depends(verify_credentials)
):
    """Execute bot command"""
    
    supported_actions = ["follow", "like", "comment", "unfollow", "analyze", "pause", "resume"]
    
    if command.action not in supported_actions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported action. Supported: {supported_actions}"
        )
    
    return {
        "status": "success",
        "action": command.action,
        "username": command.username,
        "message": f"Command {command.action} executed successfully"
    }


@app.get("/api/analytics")
async def get_analytics(username: str = Depends(verify_credentials)):
    """Get analytics data"""
    return {
        "total_actions": bot_state["total_actions"],
        "actions_by_type": {
            "follow": 0,
            "like": 0,
            "comment": 0,
            "unfollow": 0
        },
        "success_rate": 0.95,
        "active_accounts": len(bot_state["active_accounts"]),
        "last_updated": datetime.utcnow().isoformat()
    }


@app.get("/api/analytics/{account_username}")
async def get_account_analytics(
    account_username: str,
    username: str = Depends(verify_credentials)
):
    """Get analytics for specific account"""
    return {
        "username": account_username,
        "actions_today": {
            "follow": 0,
            "like": 0,
            "comment": 0,
            "unfollow": 0
        },
        "success_rate": 0.95,
        "last_action": None,
        "risk_score": 25
    }


@app.get("/api/config")
async def get_config(username: str = Depends(verify_credentials)):
    """Get bot configuration"""
    return {
        "anti_ban": {
            "enabled": os.getenv("ENABLE_HUMAN_SIMULATION", "true").lower() == "true",
            "max_follows_per_day": int(os.getenv("MAX_FOLLOWS_PER_DAY", "200")),
            "max_likes_per_day": int(os.getenv("MAX_LIKES_PER_DAY", "500")),
            "max_comments_per_day": int(os.getenv("MAX_COMMENTS_PER_DAY", "50"))
        },
        "scheduler": {
            "timezone": os.getenv("TIMEZONE", "America/Los_Angeles"),
            "peak_hours_start": int(os.getenv("PEAK_HOURS_START", "10")),
            "peak_hours_end": int(os.getenv("PEAK_HOURS_END", "21"))
        },
        "proxy": {
            "enabled": bool(os.getenv("PROXY_API_KEY", "")),
            "pool_size": int(os.getenv("PROXY_POOL_SIZE", "100"))
        }
    }


@app.post("/api/config")
async def update_config(
    config_update: Dict[str, Any],
    username: str = Depends(verify_credentials)
):
    """Update bot configuration"""
    return {
        "status": "success",
        "message": "Configuration updated successfully",
        "config": config_update
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
