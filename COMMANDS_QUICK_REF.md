# Quick Reference - Build & Deploy Commands

## 🚀 One-Line Deploy Commands

### Deploy Everything (Production)
```bash
./scripts/deploy-all.sh
```

### Using Makefile
```bash
make deploy           # Deploy both frontend & backend
make deploy-backend   # Deploy backend only
make deploy-frontend  # Deploy frontend only
```

---

## 🛠️ Build Commands

### Frontend
```bash
cd frontend && npm install && npm run build
# OR
make build-frontend
# OR
./scripts/build-frontend.sh
```

### Backend
```bash
pip install -r requirements-vercel.txt
# OR
make build-backend
# OR
./scripts/build-backend.sh
```

---

## 🧑‍💻 Development Commands

### Run Both Servers
```bash
make dev
```

### Frontend Dev Server
```bash
cd frontend && npm run dev
# Runs on http://localhost:3000
```

### Backend Dev Server
```bash
python api/index.py
# Runs on http://localhost:8000
```

---

## 📦 Vercel Direct Commands

### Backend
```bash
vercel                  # Preview
vercel --prod           # Production
vercel env add VAR      # Add env variable
vercel logs             # View logs
```

### Frontend
```bash
cd frontend
vercel                  # Preview
vercel --prod           # Production
vercel env add VAR      # Add env variable
```

---

## 🔧 Essential Makefile Commands

```bash
make help              # Show all commands
make install           # Install all dependencies
make dev               # Run development servers
make build             # Build everything
make deploy            # Deploy to production
make test              # Run tests
make clean             # Clean build artifacts
make logs              # View deployment logs
make status            # Check deployment status
```

---

## 📋 Complete Deployment Checklist

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy Backend**
   ```bash
   vercel --prod
   # Note the URL
   ```

3. **Set Backend Env Variables**
   ```bash
   vercel env add IG_ACCOUNTS production
   vercel env add DASHBOARD_USERNAME production
   vercel env add DASHBOARD_PASSWORD production
   vercel --prod  # Redeploy
   ```

4. **Deploy Frontend**
   ```bash
   cd frontend
   vercel env add NEXT_PUBLIC_API_URL production
   # Enter backend URL from step 2
   vercel --prod
   ```

5. **Test**
   ```bash
   curl https://your-backend.vercel.app/health
   ```

---

## 🚨 Troubleshooting Commands

```bash
vercel logs --follow          # Real-time logs
vercel ls                     # List deployments
vercel inspect URL            # Inspect deployment
vercel rollback URL           # Rollback deployment
make clean                    # Clean build files
```

---

## 📊 Monitoring Commands

```bash
# Backend health
curl https://your-backend.vercel.app/health

# API status
curl -u admin:password https://your-backend.vercel.app/api/status

# Analytics
curl -u admin:password https://your-backend.vercel.app/api/analytics

# Start bot
curl -X POST -u admin:password https://your-backend.vercel.app/api/bot/start

# Stop bot
curl -X POST -u admin:password https://your-backend.vercel.app/api/bot/stop
```

---

## 🎯 Most Common Workflows

### First Time Setup
```bash
make install
./scripts/deploy-all.sh
```

### Update & Redeploy
```bash
git pull
make deploy
```

### Quick Test Locally
```bash
make dev
```

### Build & Test
```bash
make build
make test
```

### View Logs
```bash
make logs
```

---

## 💡 Pro Tips

1. **Use Makefile** for consistent commands across team
2. **Use deploy-all.sh** for automated full deployment
3. **Always test locally** with `make dev` before deploying
4. **Check logs** after deployment with `make logs`
5. **Use preview deployments** for testing: `vercel` (without --prod)

---

For detailed documentation, see `BUILD_DEPLOY_COMMANDS.md`
