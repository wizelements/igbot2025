# API Reference

Complete API documentation for IGBot 2025.

## 🔐 Authentication

All protected endpoints require HTTP Basic Authentication:

```bash
curl -u username:password https://your-project.vercel.app/api/endpoint
```

Credentials are set via environment variables:
- `DASHBOARD_USERNAME` (default: admin)
- `DASHBOARD_PASSWORD` (default: changeme)

## 📍 Base URL

```
https://your-project.vercel.app
```

## 🌐 Public Endpoints

### GET /

Get API information.

**Response:**
```json
{
  "message": "IGBot 2025 API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-11T12:00:00Z",
  "version": "1.0.0",
  "environment": "production"
}
```

### GET /docs

Interactive API documentation (Swagger UI).

### GET /redoc

Alternative API documentation (ReDoc).

## 🔒 Protected Endpoints

### Account Management

#### GET /api/accounts

List all Instagram accounts.

**Response:**
```json
[
  {
    "username": "your_account",
    "status": "active",
    "is_active": true,
    "last_action": null,
    "actions_today": {
      "follow": 0,
      "like": 0,
      "comment": 0,
      "unfollow": 0
    }
  }
]
```

#### POST /api/accounts/add

Add new Instagram account.

**Request:**
```json
{
  "username": "new_account",
  "password": "password123",
  "two_fa_secret": "optional_2fa_secret"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Account new_account added successfully",
  "username": "new_account"
}
```

### Bot Control

#### POST /api/bot/start

Start the bot.

**Response:**
```json
{
  "status": "success",
  "message": "Bot started successfully",
  "timestamp": "2025-12-11T12:00:00Z"
}
```

#### POST /api/bot/stop

Stop the bot.

**Response:**
```json
{
  "status": "success",
  "message": "Bot stopped successfully",
  "timestamp": "2025-12-11T12:00:00Z"
}
```

#### GET /api/status

Get bot status.

**Response:**
```json
{
  "status": "running",
  "accounts": 1,
  "total_actions": 150,
  "uptime": "2025-12-11T10:00:00Z",
  "active_accounts": ["account1"]
}
```

#### POST /api/bot/command

Execute bot command.

**Request:**
```json
{
  "action": "follow",
  "username": "account1",
  "params": {
    "target": "@someone"
  }
}
```

**Supported Actions:**
- `follow` - Follow users
- `like` - Like posts
- `comment` - Comment on posts
- `unfollow` - Unfollow users
- `analyze` - Run analytics
- `pause` - Pause bot
- `resume` - Resume bot

**Response:**
```json
{
  "status": "success",
  "action": "follow",
  "username": "account1",
  "message": "Command follow executed successfully"
}
```

### Analytics

#### GET /api/analytics

Get global analytics.

**Response:**
```json
{
  "total_actions": 500,
  "actions_by_type": {
    "follow": 100,
    "like": 250,
    "comment": 50,
    "unfollow": 100
  },
  "success_rate": 0.95,
  "active_accounts": 1,
  "last_updated": "2025-12-11T12:00:00Z"
}
```

#### GET /api/analytics/{username}

Get account-specific analytics.

**Parameters:**
- `username` (path) - Instagram username

**Response:**
```json
{
  "username": "account1",
  "actions_today": {
    "follow": 50,
    "like": 100,
    "comment": 20,
    "unfollow": 30
  },
  "success_rate": 0.95,
  "last_action": "2025-12-11T11:55:00Z",
  "risk_score": 25
}
```

### Configuration

#### GET /api/config

Get bot configuration.

**Response:**
```json
{
  "anti_ban": {
    "enabled": true,
    "max_follows_per_day": 200,
    "max_likes_per_day": 500,
    "max_comments_per_day": 50
  },
  "scheduler": {
    "timezone": "America/Los_Angeles",
    "peak_hours_start": 10,
    "peak_hours_end": 21
  },
  "proxy": {
    "enabled": true,
    "pool_size": 100
  }
}
```

#### POST /api/config

Update bot configuration.

**Request:**
```json
{
  "anti_ban": {
    "max_follows_per_day": 150
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Configuration updated successfully",
  "config": {
    "anti_ban": {
      "max_follows_per_day": 150
    }
  }
}
```

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## 🔗 Rate Limits

API endpoints have the following rate limits:

- General endpoints: 100 requests/minute
- Bot commands: 30 requests/minute
- Analytics: 60 requests/minute

## 📝 Examples

### Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

base_url = "https://your-project.vercel.app"
auth = HTTPBasicAuth("admin", "your_password")

# Start bot
response = requests.post(f"{base_url}/api/bot/start", auth=auth)
print(response.json())

# Get analytics
response = requests.get(f"{base_url}/api/analytics", auth=auth)
print(response.json())
```

### JavaScript Example

```javascript
const baseUrl = "https://your-project.vercel.app";
const auth = btoa("admin:your_password");

// Start bot
fetch(`${baseUrl}/api/bot/start`, {
  method: "POST",
  headers: {
    "Authorization": `Basic ${auth}`
  }
})
  .then(res => res.json())
  .then(data => console.log(data));

// Get analytics
fetch(`${baseUrl}/api/analytics`, {
  headers: {
    "Authorization": `Basic ${auth}`
  }
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### cURL Examples

```bash
# Start bot
curl -X POST https://your-project.vercel.app/api/bot/start \
  -u admin:password

# Get status
curl https://your-project.vercel.app/api/status \
  -u admin:password

# Execute command
curl -X POST https://your-project.vercel.app/api/bot/command \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{"action":"follow","username":"account1"}'

# Get analytics
curl https://your-project.vercel.app/api/analytics \
  -u admin:password
```

## 🔧 Error Handling

All errors return JSON with the following structure:

```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2025-12-11T12:00:00Z"
}
```

## 📚 Additional Resources

- Interactive docs: `/docs`
- ReDoc: `/redoc`
- GitHub: https://github.com/yourusername/igbot2025
- Issues: https://github.com/yourusername/igbot2025/issues
