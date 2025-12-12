# 🚀 Start Here - Deploy IGBot 2025

> **Quick deploy your Instagram bot in 3 minutes!**

---

## ⚡ Fastest Way (3 minutes)

```bash
# Step 1: Install Vercel CLI
npm install -g vercel
vercel login

# Step 2: Deploy everything
./scripts/deploy-all.sh

# Step 3: Verify
./scripts/verify-deployment.sh
```

**Done!** Your bot is live! 🎉

---

## 📚 Choose Your Method

### 1. 🤖 Automated Script (Recommended)
Perfect for: First-time users, quick deployments

```bash
./scripts/deploy-all.sh
```

**Features:**
- ✅ Deploys backend & frontend
- ✅ Configures environment variables
- ✅ Runs health checks
- ✅ Shows deployment URLs

---

### 2. 🛠️ Makefile (Flexible)
Perfect for: Developers, repeated deployments

```bash
# See all commands
make help

# Deploy everything
make deploy

# Deploy just frontend
make deploy-frontend

# Deploy just backend
make deploy-backend
```

**Features:**
- ✅ Universal commands
- ✅ Build & deploy separately
- ✅ Development mode
- ✅ Utility commands

---

### 3. 🎮 Manual Control (Advanced)
Perfect for: Custom configurations, debugging

```bash
# Deploy backend
vercel --prod

# Deploy frontend
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
vercel --prod
```

**Features:**
- ✅ Full control
- ✅ Step-by-step process
- ✅ Custom configuration

---

## 📖 Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **COMMANDS_QUICK_REF.md** | Quick command lookup | Need a command fast |
| **BUILD_DEPLOY_COMMANDS.md** | Complete deployment guide | First time setup |
| **BUILD_SYSTEM_SUMMARY.md** | System overview | Understanding system |
| **DEPLOYMENT_FLOWCHART.md** | Visual workflows | Visual learner |
| **BUILD_COMPLETE.md** | Feature list & status | See what's available |

---

## 🎯 Common Tasks

### First Time Deployment
```bash
./scripts/deploy-all.sh
```

### Development
```bash
make dev
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Update Deployment
```bash
git pull
make deploy
```

### Check Logs
```bash
make logs
```

### Verify Deployment
```bash
./scripts/verify-deployment.sh
```

---

## 🔐 Environment Variables Needed

### Backend (Required)
```
IG_ACCOUNTS=username:password:2fa_secret
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password
```

### Frontend (Required)
```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

**The automated script will help you set these up!**

---

## ✅ What You Get

After deployment, you'll have:

✅ **Backend API** - FastAPI with all endpoints  
✅ **Frontend Dashboard** - Next.js web interface  
✅ **Auto-configured** - Environment variables set  
✅ **Health checked** - All endpoints verified  
✅ **Ready to use** - Start botting immediately  

---

## 🆘 Need Help?

### Quick Help
```bash
make help  # See all available commands
```

### Documentation
1. Start with **COMMANDS_QUICK_REF.md**
2. Read **BUILD_DEPLOY_COMMANDS.md** for details
3. Check **DEPLOYMENT_FLOWCHART.md** for visual guide

### Common Issues

**Build failed?**
```bash
make clean
make build
```

**Deployment failed?**
```bash
make logs
make status
```

**Can't connect?**
```bash
# Update API URL
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
vercel --prod
```

---

## 🎉 Success Checklist

After deployment, verify:

- [ ] Backend health check passes: `curl https://your-api.vercel.app/health`
- [ ] Frontend loads in browser
- [ ] Can login to dashboard
- [ ] Environment variables are set
- [ ] Bot can start/stop
- [ ] Analytics are visible

---

## 🚀 Ready to Deploy?

Choose your method:

```bash
# Fastest (recommended for first time)
./scripts/deploy-all.sh

# Flexible (recommended for development)
make deploy

# Manual (recommended for custom setup)
vercel --prod && cd frontend && vercel --prod
```

---

## 📋 All Available Commands

### Makefile Commands
```bash
make help              # Show all commands
make install           # Install dependencies
make dev               # Start dev servers
make build             # Build everything
make deploy            # Deploy to production
make logs              # View logs
make status            # Check status
make clean             # Clean build files
```

### NPM Scripts (Frontend)
```bash
cd frontend
npm run dev            # Development server
npm run build          # Production build
npm run deploy         # Deploy to production
npm run clean          # Clean build
```

### Shell Scripts
```bash
./scripts/deploy-all.sh         # Full deployment
./scripts/build-frontend.sh     # Build frontend
./scripts/build-backend.sh      # Build backend
./scripts/verify-deployment.sh  # Verify deployment
```

---

## 💡 Pro Tips

1. **Always test locally first**
   ```bash
   make dev
   ```

2. **Use preview deployments for testing**
   ```bash
   vercel  # Without --prod
   ```

3. **Check logs after deployment**
   ```bash
   make logs
   ```

4. **Verify everything works**
   ```bash
   ./scripts/verify-deployment.sh
   ```

5. **Keep environment variables secure**
   - Never commit to git
   - Use strong passwords

---

## 📞 Support Resources

- **Quick Reference**: `COMMANDS_QUICK_REF.md`
- **Full Guide**: `BUILD_DEPLOY_COMMANDS.md`
- **Visual Guide**: `DEPLOYMENT_FLOWCHART.md`
- **System Details**: `BUILD_SYSTEM_SUMMARY.md`
- **Feature List**: `BUILD_COMPLETE.md`

---

## ⏱️ Time Estimates

| Method | Time | Difficulty |
|--------|------|------------|
| Automated Script | 3-5 min | Easy |
| Makefile | 5-10 min | Medium |
| Manual | 10-15 min | Advanced |

---

## 🎊 Let's Go!

Pick your favorite method and deploy now:

```bash
./scripts/deploy-all.sh
```

**Happy Deploying! 🚀**

---

*Generated with [Continue](https://continue.dev)*  
*Co-Authored-By: Continue <noreply@continue.dev>*
