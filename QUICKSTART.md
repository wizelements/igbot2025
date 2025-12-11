# 🚀 Quick Start Guide - 5 Minutes to Deploy

Get your Instagram bot running on Vercel in 5 minutes!

## ⚡ Prerequisites

- [ ] Vercel account (free): https://vercel.com/signup
- [ ] Instagram account credentials
- [ ] Node.js installed (for Vercel CLI)

## 📦 Step 1: Install Vercel CLI (1 minute)

```bash
npm install -g vercel
vercel login
```

## 🔧 Step 2: Deploy (2 minutes)

From the project directory:

```bash
vercel --prod
```

Follow the prompts:
- Project name: `igbot2025`
- Directory: `./`
- Override settings: `No`

## 🔐 Step 3: Configure (2 minutes)

### Via Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select your project
3. Settings → Environment Variables
4. Add:

```
IG_ACCOUNTS=your_username:your_password
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password
```

5. Redeploy:

```bash
vercel --prod
```

## ✅ Step 4: Test

Visit: `https://your-project.vercel.app/docs`

Or test via curl:

```bash
# Health check
curl https://your-project.vercel.app/health

# Start bot
curl -X POST https://your-project.vercel.app/api/bot/start \
  -u admin:your_password
```

## 🎉 You're Done!

Your bot is now live!

### Next Steps:

1. **Monitor**: Check `/api/status` for bot status
2. **Analytics**: View `/api/analytics` for metrics
3. **Configure**: Adjust settings via `/api/config`
4. **Secure**: Change default passwords
5. **Optimize**: Add proxy for better performance

## 📚 Learn More

- Full docs: `README.md`
- Deployment guide: `DEPLOYMENT.md`
- API reference: `https://your-project.vercel.app/docs`

## 🆘 Need Help?

Common issues:

**"Module not found"**
- Ensure `requirements-vercel.txt` exists
- Check `runtime.txt` has `python-3.11`

**"Authentication failed"**
- Verify credentials in environment variables
- Check Instagram login works manually

**"Rate limit exceeded"**
- Normal - bot respects Instagram limits
- Adjust limits in configuration

## 💬 Support

- GitHub Issues: Report bugs
- Discussions: Ask questions
- Docs: Check documentation

---

**Happy Botting! 🤖**
