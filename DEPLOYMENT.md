# Vercel Deployment Guide for IGBot 2025

This guide walks you through deploying IGBot 2025 to Vercel step-by-step.

## 📋 Pre-Deployment Checklist

- [ ] Vercel account created (https://vercel.com)
- [ ] Node.js and npm installed (for Vercel CLI)
- [ ] Instagram account credentials ready
- [ ] Git repository initialized
- [ ] Environment variables prepared

## 🚀 Deployment Steps

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

Choose your preferred login method (GitHub, GitLab, Bitbucket, or Email).

### Step 3: Initialize Project

From the project root directory:

```bash
cd /workspaces/igbot2025-1
vercel
```

You'll be prompted with:

```
? Set up and deploy "~/igbot2025-1"? [Y/n] Y
? Which scope do you want to deploy to? [Your Account]
? Link to existing project? [y/N] N
? What's your project's name? igbot2025
? In which directory is your code located? ./
```

### Step 4: Configure Environment Variables

#### Option A: Via Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select your project (igbot2025)
3. Click "Settings" → "Environment Variables"
4. Add each variable from `.env.production`

**Minimum Required Variables:**

```
IG_ACCOUNTS=your_username:your_password:optional_2fa_secret
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password_here
ENVIRONMENT=production
```

**Recommended Variables:**

```
PROXY_API_KEY=your_proxy_key
TIMEZONE=America/Los_Angeles
MAX_FOLLOWS_PER_DAY=200
MAX_LIKES_PER_DAY=500
MAX_COMMENTS_PER_DAY=50
ENABLE_HUMAN_SIMULATION=true
```

#### Option B: Via CLI

```bash
vercel env add IG_ACCOUNTS
# Enter value when prompted

vercel env add DASHBOARD_USERNAME
# Enter value when prompted

vercel env add DASHBOARD_PASSWORD
# Enter value when prompted
```

### Step 5: Deploy to Production

```bash
vercel --prod
```

Wait for deployment to complete. You'll get a URL like:
```
https://igbot2025.vercel.app
```

### Step 6: Verify Deployment

Test your deployment:

```bash
# Health check
curl https://your-project.vercel.app/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0","environment":"production"}
```

### Step 7: Test Authentication

```bash
# Test with your credentials
curl https://your-project.vercel.app/api/status \
  -u admin:your_password
```

### Step 8: Access API Documentation

Visit: `https://your-project.vercel.app/docs`

This provides interactive API documentation.

## 🔧 Post-Deployment Configuration

### Set Up Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Configure Alerts

1. Settings → Integrations
2. Add Slack, Discord, or email notifications
3. Configure for deployment status

### Set Up Monitoring

Add these optional monitoring services:

**Sentry (Error Tracking):**
```bash
vercel env add SENTRY_DSN
# Enter your Sentry DSN
```

**Prometheus (Metrics):**
```bash
vercel env add ENABLE_METRICS
# Enter: true
```

## 📊 Testing Your Deployment

### 1. Start the Bot

```bash
curl -X POST https://your-project.vercel.app/api/bot/start \
  -u admin:your_password
```

Expected response:
```json
{
  "status": "success",
  "message": "Bot started successfully",
  "timestamp": "2025-12-11T..."
}
```

### 2. Check Status

```bash
curl https://your-project.vercel.app/api/status \
  -u admin:your_password
```

### 3. View Analytics

```bash
curl https://your-project.vercel.app/api/analytics \
  -u admin:your_password
```

### 4. Get Configuration

```bash
curl https://your-project.vercel.app/api/config \
  -u admin:your_password
```

## 🐛 Troubleshooting

### Issue: Deployment Fails

**Check build logs:**
```bash
vercel logs
```

**Common fixes:**
- Ensure `requirements-vercel.txt` exists
- Check `runtime.txt` has correct Python version
- Verify `vercel.json` syntax

### Issue: 500 Internal Server Error

**View runtime logs:**
```bash
vercel logs --follow
```

**Common causes:**
- Missing environment variables
- Invalid Instagram credentials
- Module import errors

### Issue: Authentication Not Working

**Verify environment variables:**
```bash
vercel env ls
```

**Ensure these are set:**
- `DASHBOARD_USERNAME`
- `DASHBOARD_PASSWORD`

### Issue: Bot Not Performing Actions

**Check:**
1. Instagram credentials are correct
2. Accounts aren't rate-limited
3. Proxy settings (if enabled)

**View logs:**
```bash
vercel logs --follow
```

## 🔄 Updating Your Deployment

### Update Code

```bash
git add .
git commit -m "Update bot logic"
git push origin main

# Vercel auto-deploys if connected to Git
# Or manually deploy:
vercel --prod
```

### Update Environment Variables

```bash
vercel env rm VARIABLE_NAME
vercel env add VARIABLE_NAME
```

Then redeploy:
```bash
vercel --prod
```

## 🔐 Security Checklist

- [ ] Changed default dashboard password
- [ ] Enabled 2FA on Instagram accounts
- [ ] Using strong, unique passwords
- [ ] Environment variables set in Vercel (not in code)
- [ ] `.env` files not committed to Git
- [ ] Proxy service configured (recommended)
- [ ] Rate limits configured appropriately
- [ ] Monitoring/alerts enabled

## 📈 Performance Optimization

### Vercel Function Settings

Optimal settings in `vercel.json`:
```json
{
  "functions": {
    "api/index.py": {
      "memory": 3008,
      "maxDuration": 300
    }
  }
}
```

### Database Recommendations

For production use, consider external services:

- **MongoDB Atlas**: For document storage
- **Redis Labs**: For caching and queues
- **Supabase**: For relational data

Add connection strings to environment variables.

## 🌍 Multi-Region Deployment

Deploy to multiple regions for better performance:

```json
{
  "regions": ["iad1", "sfo1", "lhr1"]
}
```

Available regions:
- `iad1` - Washington, D.C., USA
- `sfo1` - San Francisco, USA
- `lhr1` - London, UK
- `hnd1` - Tokyo, Japan
- `gru1` - São Paulo, Brazil

## 📞 Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **GitHub Issues**: Create an issue in your repository
- **Community Discord**: Join Vercel's community

## 🎉 Success!

Your Instagram bot is now deployed and running on Vercel!

**Next Steps:**
1. Monitor analytics regularly
2. Adjust rate limits based on account age
3. Set up alerts for issues
4. Review logs periodically
5. Keep dependencies updated

---

**Need Help?** Check the main README.md or open an issue on GitHub.
