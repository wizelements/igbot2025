# IGBot 2025 - Advanced Instagram Automation Bot

🤖 A sophisticated Instagram automation bot with AI-powered features, anti-ban protection, and enterprise-grade scalability.

## 🚀 Features

- **Multi-Account Management**: Run multiple Instagram accounts simultaneously
- **Anti-Ban Protection**: Human-like behavior simulation, warmup periods, action limits
- **Intelligent Scheduling**: Peak hours optimization, timezone-aware actions
- **Proxy Rotation**: Built-in proxy support for enhanced security
- **Analytics Dashboard**: Real-time monitoring and performance tracking
- **Auto Follow/Unfollow**: Targeted user engagement
- **Smart Liking & Commenting**: AI-powered content interaction
- **Hashtag Research**: Find trending hashtags for maximum reach
- **Emergency Controls**: Kill switch and auto-pause on anomalies

## 📋 Prerequisites

- Python 3.11+
- Vercel Account (for deployment)
- Instagram Account(s)
- Optional: Proxy service, MongoDB, Redis

## 🔧 Quick Start - Vercel Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Clone and Configure

```bash
git clone <your-repo-url>
cd igbot2025-1
```

### 3. Deploy to Vercel

```bash
vercel
```

Follow the prompts:
- Set up and deploy: **Yes**
- Which scope: Select your account
- Link to existing project: **No**
- Project name: **igbot2025**
- Directory: **./** (current directory)
- Override settings: **No**

### 4. Configure Environment Variables

Go to your Vercel Dashboard → Project Settings → Environment Variables

Add the following (see `.env.production` for full list):

**Required:**
```
IG_ACCOUNTS=username:password:2fa_secret
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password
```

**Recommended:**
```
PROXY_API_KEY=your_proxy_key
TIMEZONE=America/Los_Angeles
MAX_FOLLOWS_PER_DAY=200
MAX_LIKES_PER_DAY=500
```

### 5. Redeploy with Environment Variables

```bash
vercel --prod
```

## 🌐 API Endpoints

Once deployed, your bot will be available at: `https://your-project.vercel.app`

### Public Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Protected Endpoints (Basic Auth Required)

#### Account Management
- `GET /api/accounts` - List all accounts
- `POST /api/accounts/add` - Add new account

#### Bot Control
- `POST /api/bot/start` - Start bot
- `POST /api/bot/stop` - Stop bot
- `POST /api/bot/command` - Execute command
- `GET /api/status` - Get bot status

#### Analytics
- `GET /api/analytics` - Global analytics
- `GET /api/analytics/{username}` - Account-specific analytics

#### Configuration
- `GET /api/config` - Get configuration
- `POST /api/config` - Update configuration

## 📊 Usage Examples

### Start Bot via API

```bash
curl -X POST https://your-project.vercel.app/api/bot/start \
  -u admin:your_password
```

### Get Analytics

```bash
curl https://your-project.vercel.app/api/analytics \
  -u admin:your_password
```

### Execute Command

```bash
curl -X POST https://your-project.vercel.app/api/bot/command \
  -u admin:your_password \
  -H "Content-Type: application/json" \
  -d '{
    "action": "follow",
    "username": "your_ig_account"
  }'
```

## 🔐 Security Best Practices

1. **Strong Passwords**: Use unique, strong passwords for dashboard access
2. **2FA**: Enable 2FA on Instagram accounts
3. **Proxies**: Use residential proxies for better security
4. **Rate Limits**: Respect Instagram's limits (configured by default)
5. **Environment Variables**: Never commit sensitive data
6. **Regular Monitoring**: Check analytics for anomalies

## 🛡️ Anti-Ban Features

- **Human Simulation**: Random delays, typing patterns, mouse movements
- **Warmup Period**: Gradual action increase for new accounts
- **Action Limits**: Daily limits per action type
- **Peak Hours**: Activity during high-engagement times
- **Shadowban Detection**: Automatic pause if shadowban detected
- **Proxy Rotation**: Change IP addresses regularly

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IG_ACCOUNTS` | Instagram accounts (username:password:2fa) | - |
| `DASHBOARD_USERNAME` | Dashboard login username | admin |
| `DASHBOARD_PASSWORD` | Dashboard login password | changeme |
| `MAX_FOLLOWS_PER_DAY` | Maximum follows per day | 200 |
| `MAX_LIKES_PER_DAY` | Maximum likes per day | 500 |
| `MAX_COMMENTS_PER_DAY` | Maximum comments per day | 50 |
| `TIMEZONE` | Bot timezone | America/Los_Angeles |
| `PROXY_API_KEY` | Proxy service API key | - |

See `.env.production` for complete list.

## 📈 Analytics & Monitoring

The bot tracks:
- Total actions performed
- Success/failure rates
- Ban risk scores
- Account health metrics
- Performance over time

Access via:
- API endpoints (`/api/analytics`)
- Web dashboard (coming soon)
- Prometheus metrics (optional)

## 🚨 Emergency Controls

### Kill Switch
Immediately stop all bot activities:
```bash
curl -X POST https://your-project.vercel.app/api/bot/stop \
  -u admin:your_password
```

### Auto-Pause
Bot automatically pauses when:
- Ban risk score exceeds threshold
- Success rate drops below minimum
- Shadowban detected
- Rate limit hit

## 🔄 Advanced Features

### Multi-Account Management
Run multiple Instagram accounts with independent schedules and limits.

### Proxy Rotation
Automatic proxy rotation for enhanced anonymity:
```
PROXY_API_KEY=your_key
PROXY_POOL_SIZE=100
PROXY_ROTATION_INTERVAL=300
```

### AI Content Generation (Optional)
```
OPENAI_API_KEY=your_key
AUTO_REMIX_REELS=true
FYP_OPTIMIZATION=true
```

## 🐛 Troubleshooting

### Bot Not Starting
1. Check environment variables are set
2. Verify Instagram credentials
3. Check Vercel logs: `vercel logs`

### Actions Not Working
1. Check rate limits haven't been hit
2. Verify account isn't shadowbanned
3. Ensure proxies are working (if enabled)

### Authentication Errors
1. Verify Instagram password is correct
2. Add 2FA secret if 2FA is enabled
3. Try logging in manually first

## 📝 Local Development

For local testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python api/index.py
```

Visit: http://localhost:8000/docs

## 🔗 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Instagram API Guide](https://github.com/adw0rd/instagrapi)

## ⚠️ Disclaimer

This bot is for educational purposes. Use responsibly and respect Instagram's Terms of Service. Automation may violate Instagram's policies and could result in account suspension.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues and questions:
- Open a GitHub issue
- Check documentation
- Review Vercel logs

---

Built with ❤️ using FastAPI and Vercel

**Happy Botting! 🚀**
