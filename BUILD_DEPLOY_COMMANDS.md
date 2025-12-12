# Build & Deployment Commands

Complete guide for building and deploying the IGBot 2025 project.

---

## 🎯 Quick Commands

### Frontend Development
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run API locally
python api/index.py

# Test API
python test_api.py

# Install Vercel dependencies
pip install -r requirements-vercel.txt
```

---

## 🚀 Full Deployment Setup

### 1. Prerequisites
```bash
# Install Vercel CLI globally
npm install -g vercel

# Verify installation
vercel --version

# Login to Vercel
vercel login
```

### 2. Backend API Deployment (Python/FastAPI)

#### Deploy Backend
```bash
# From project root
vercel

# Or deploy to production directly
vercel --prod
```

#### Set Backend Environment Variables
```bash
# Interactive method
vercel env add IG_ACCOUNTS
vercel env add DASHBOARD_USERNAME
vercel env add DASHBOARD_PASSWORD

# Or via Vercel Dashboard:
# https://vercel.com/dashboard → Your Project → Settings → Environment Variables
```

#### Required Backend Environment Variables
```bash
IG_ACCOUNTS=username:password:2fa_secret
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password
MAX_FOLLOWS_PER_DAY=200
MAX_LIKES_PER_DAY=500
MAX_COMMENTS_PER_DAY=50
TIMEZONE=America/Los_Angeles
```

### 3. Frontend Dashboard Deployment (Next.js)

#### Deploy Frontend
```bash
# Navigate to frontend directory
cd frontend

# Deploy to Vercel
vercel

# Or deploy to production
vercel --prod
```

#### Set Frontend Environment Variables
```bash
# Add API URL (use your backend deployment URL)
vercel env add NEXT_PUBLIC_API_URL

# Example value:
# https://your-backend-project.vercel.app
```

#### Build Frontend Locally
```bash
cd frontend
npm install
npm run build
```

---

## 🔧 Complete Deployment Script

### Automated Deployment
```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

### Manual Full Stack Deployment

#### Step 1: Deploy Backend
```bash
# From project root
echo "Deploying Backend API..."
vercel --prod

# Note the deployment URL
# Example: https://igbot2025-api.vercel.app
```

#### Step 2: Configure Backend
```bash
# Set environment variables
vercel env add IG_ACCOUNTS production
vercel env add DASHBOARD_USERNAME production
vercel env add DASHBOARD_PASSWORD production

# Redeploy with new env vars
vercel --prod
```

#### Step 3: Deploy Frontend
```bash
# Navigate to frontend
cd frontend

# Set API URL (use backend URL from Step 1)
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://igbot2025-api.vercel.app

# Deploy frontend
vercel --prod

# Note the frontend URL
# Example: https://igbot2025-dashboard.vercel.app
```

---

## 📦 Build Commands Reference

### Backend Build Commands
```bash
# Install dependencies
pip install -r requirements-vercel.txt

# Build (handled by Vercel)
echo 'Python build complete'

# Local test
uvicorn api.index:app --reload
```

### Frontend Build Commands
```bash
# Install dependencies
npm install

# Build Next.js
npm run build

# Export static files (if using static export)
npm run build

# Start production
npm start
```

---

## 🌐 Deployment URLs

After deployment, you'll have two URLs:

### Backend API
```
Production: https://your-backend.vercel.app
Endpoints:
  - GET  /                    (API Info)
  - GET  /health              (Health Check)
  - GET  /docs                (API Documentation)
  - POST /api/bot/start       (Start Bot)
  - POST /api/bot/stop        (Stop Bot)
  - GET  /api/analytics       (Analytics)
  - GET  /api/accounts        (List Accounts)
```

### Frontend Dashboard
```
Production: https://your-frontend.vercel.app
Pages:
  - /                         (Home)
  - /login                    (Login)
  - /dashboard                (Overview)
  - /dashboard/accounts       (Accounts)
  - /dashboard/actions        (Actions)
  - /dashboard/analytics      (Analytics)
  - /dashboard/settings       (Settings)
```

---

## 🔄 Update & Redeploy

### Backend Updates
```bash
# Make changes to code
git add .
git commit -m "Update backend"
git push

# Redeploy
vercel --prod

# Or use automatic Git integration
# (Connect repo in Vercel Dashboard)
```

### Frontend Updates
```bash
cd frontend

# Make changes to code
git add .
git commit -m "Update frontend"
git push

# Redeploy
vercel --prod
```

---

## 🧪 Testing Deployments

### Test Backend
```bash
# Health check
curl https://your-backend.vercel.app/health

# API docs
curl https://your-backend.vercel.app/docs

# Protected endpoint
curl -u admin:password https://your-backend.vercel.app/api/status
```

### Test Frontend
```bash
# Open in browser
open https://your-frontend.vercel.app

# Or use curl
curl https://your-frontend.vercel.app
```

---

## 🐛 Troubleshooting

### View Backend Logs
```bash
vercel logs

# Follow logs in real-time
vercel logs --follow
```

### View Frontend Logs
```bash
cd frontend
vercel logs

# Follow logs
vercel logs --follow
```

### Check Deployment Status
```bash
# List all deployments
vercel ls

# Get specific deployment info
vercel inspect <deployment-url>
```

### Rollback Deployment
```bash
# List previous deployments
vercel ls

# Promote a previous deployment to production
vercel promote <deployment-url>
```

---

## 🔐 Security Checklist

### Before Deployment
- [ ] Update `DASHBOARD_PASSWORD` to strong password
- [ ] Add valid Instagram credentials
- [ ] Configure 2FA secrets if enabled
- [ ] Set up proxies (if using)
- [ ] Review rate limits
- [ ] Test locally first

### After Deployment
- [ ] Verify all environment variables are set
- [ ] Test API endpoints
- [ ] Test frontend login
- [ ] Check bot can start/stop
- [ ] Monitor initial analytics
- [ ] Set up alerts (optional)

---

## 🎛️ Environment Variables

### Backend (.env or Vercel)
```bash
# Required
IG_ACCOUNTS=username:password:2fa_secret
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=secure_password_here

# Optional Bot Settings
MAX_FOLLOWS_PER_DAY=200
MAX_LIKES_PER_DAY=500
MAX_COMMENTS_PER_DAY=50
MAX_UNFOLLOWS_PER_DAY=200
TIMEZONE=America/Los_Angeles

# Optional Features
PROXY_API_KEY=your_proxy_key
PROXY_POOL_SIZE=100
MONGODB_URI=mongodb://...
REDIS_URL=redis://...
OPENAI_API_KEY=sk-...

# Optional Security
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Frontend (.env.local or Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

---

## 📊 Monitoring

### Check Bot Status
```bash
# API status
curl -u admin:password https://your-backend.vercel.app/api/status

# Analytics
curl -u admin:password https://your-backend.vercel.app/api/analytics
```

### Vercel Analytics
```bash
# View in dashboard
vercel --prod

# Or visit:
# https://vercel.com/dashboard → Your Project → Analytics
```

---

## 🚨 Emergency Commands

### Stop Bot Immediately
```bash
curl -X POST -u admin:password \
  https://your-backend.vercel.app/api/bot/stop
```

### Check Health
```bash
curl https://your-backend.vercel.app/health
```

### View Logs
```bash
vercel logs --follow
```

---

## 📝 CI/CD Setup (Optional)

### GitHub Actions
```bash
# Already configured in .github/workflows/vercel-deploy.yml

# Add secrets to GitHub:
# Settings → Secrets → Actions:
# - VERCEL_TOKEN
# - VERCEL_ORG_ID
# - VERCEL_PROJECT_ID
```

### Automatic Deployments
```bash
# Connect Git repository in Vercel Dashboard
# Settings → Git → Connect Repository

# Now every push to main deploys automatically!
```

---

## 🎉 Quick Start Commands

### Complete New Deployment
```bash
# 1. Install CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy backend
vercel --prod

# 4. Set backend env vars
vercel env add IG_ACCOUNTS production
vercel env add DASHBOARD_USERNAME production
vercel env add DASHBOARD_PASSWORD production

# 5. Deploy frontend
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
vercel --prod

# 6. Test
curl https://your-backend.vercel.app/health
```

### Update Existing Deployment
```bash
# Pull latest changes
git pull

# Redeploy backend
vercel --prod

# Redeploy frontend
cd frontend
vercel --prod
```

---

## 📚 Additional Resources

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI on Vercel](https://vercel.com/docs/frameworks/fastapi)
- [Environment Variables Guide](https://vercel.com/docs/concepts/projects/environment-variables)

---

**Need Help?** Check `DEPLOYMENT.md` or open an issue on GitHub.
