# 🚀 Deployment Checklist

Use this checklist to ensure a smooth deployment to Vercel.

## ✅ Pre-Deployment

### Environment Setup
- [ ] Node.js installed (v16 or higher)
- [ ] Vercel CLI installed (`npm install -g vercel`)
- [ ] Vercel account created
- [ ] Git repository initialized
- [ ] Instagram account credentials ready

### File Verification
- [ ] `vercel.json` exists
- [ ] `api/index.py` exists
- [ ] `requirements.txt` exists
- [ ] `runtime.txt` exists (contains `python-3.11`)
- [ ] `.vercelignore` exists
- [ ] All documentation files present

### Security
- [ ] Changed default dashboard password
- [ ] Strong passwords prepared
- [ ] 2FA enabled on Instagram accounts (if applicable)
- [ ] `.env` files in `.gitignore`
- [ ] No secrets committed to Git

## 🔧 Deployment Steps

### 1. Local Testing
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Set local environment variables
- [ ] Ran API locally: `python api/index.py`
- [ ] Tested endpoints: `python test_api.py`
- [ ] Visited `/docs` at http://localhost:8000/docs
- [ ] All tests pass

### 2. Initial Deployment
- [ ] Logged into Vercel: `vercel login`
- [ ] Ran initial deployment: `vercel`
- [ ] Project created successfully
- [ ] Received deployment URL
- [ ] Health check works: `/health`

### 3. Environment Variables
- [ ] Opened Vercel Dashboard
- [ ] Navigated to Project Settings
- [ ] Added `IG_ACCOUNTS`
- [ ] Added `DASHBOARD_USERNAME`
- [ ] Added `DASHBOARD_PASSWORD`
- [ ] Added `ENVIRONMENT=production`
- [ ] Added optional variables (proxy, timezone, etc.)
- [ ] Saved all variables

### 4. Production Deployment
- [ ] Redeployed with: `vercel --prod`
- [ ] Deployment successful
- [ ] Production URL received
- [ ] No build errors

## ✅ Post-Deployment

### Verification
- [ ] Health endpoint works: `curl https://your-project.vercel.app/health`
- [ ] Root endpoint works: `curl https://your-project.vercel.app/`
- [ ] Docs accessible: `https://your-project.vercel.app/docs`
- [ ] Authentication works: Test with `/api/status`
- [ ] Bot starts: `POST /api/bot/start`
- [ ] Analytics available: `GET /api/analytics`

### Configuration
- [ ] Bot configuration verified: `GET /api/config`
- [ ] Rate limits appropriate for account age
- [ ] Timezone set correctly
- [ ] Proxy configured (if using)
- [ ] Emergency controls understood

### Monitoring Setup
- [ ] Bookmarked deployment URL
- [ ] Set up log monitoring: `vercel logs --follow`
- [ ] Configured alerts (optional)
- [ ] Sentry/monitoring service (optional)
- [ ] Prometheus metrics (optional)

### Documentation
- [ ] README.md reviewed
- [ ] API documentation accessible
- [ ] Deployment guide saved
- [ ] Emergency procedures understood
- [ ] Support resources bookmarked

## 🎯 First Run

### Initial Bot Startup
- [ ] Start bot: `POST /api/bot/start`
- [ ] Verify status: `GET /api/status`
- [ ] Check accounts: `GET /api/accounts`
- [ ] Monitor for 15 minutes
- [ ] Check analytics: `GET /api/analytics`
- [ ] Review logs: `vercel logs`

### Troubleshooting (if needed)
- [ ] Check Vercel logs for errors
- [ ] Verify environment variables
- [ ] Test Instagram credentials manually
- [ ] Check rate limits
- [ ] Verify proxy settings (if enabled)

## 📊 Monitoring Plan

### Daily Checks (First Week)
- [ ] Check bot status
- [ ] Review analytics
- [ ] Verify no errors in logs
- [ ] Monitor Instagram account health
- [ ] Check ban risk score

### Weekly Checks
- [ ] Review performance metrics
- [ ] Adjust rate limits if needed
- [ ] Check success rates
- [ ] Update configuration as needed
- [ ] Review and respond to any issues

### Monthly
- [ ] Review overall performance
- [ ] Update dependencies
- [ ] Security audit
- [ ] Cost analysis
- [ ] Optimization opportunities

## 🚨 Emergency Contacts

### Stop Bot Immediately
```bash
curl -X POST https://your-project.vercel.app/api/bot/stop -u admin:password
```

### Check Status
```bash
curl https://your-project.vercel.app/api/status -u admin:password
```

### View Logs
```bash
vercel logs --follow
```

### Rollback Deployment
```bash
vercel rollback
```

## 📝 Notes

### Deployment URL
```
Production: https://_________________.vercel.app
```

### Credentials
```
Dashboard Username: _______________
Dashboard Password: _______________
Instagram Account: _______________
```

### Important Dates
```
Deployment Date: _______________
Last Update: _______________
Next Review: _______________
```

## ✅ Sign-Off

Deployment completed by: _______________
Date: _______________
Version: 1.0.0

**Status: [ ] Development [ ] Staging [ ] Production**

---

## 🎉 Success!

Once all items are checked, your IGBot 2025 is successfully deployed!

**Quick Reference:**
- Docs: `https://your-project.vercel.app/docs`
- Health: `https://your-project.vercel.app/health`
- Status: `https://your-project.vercel.app/api/status`

**Happy Botting! 🤖**
