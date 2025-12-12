# 🔧 Deployment Fix - Separate Projects

## ⚠️ Important: Backend and Frontend are Separate Projects

The backend (Python API) and frontend (Next.js) need to be deployed as **two separate Vercel projects**.

---

## 🎯 Correct Deployment Process

### Step 1: Deploy Backend (Python API)

```bash
# From project root
vercel --prod

# When prompted:
# - Set up and deploy: Yes
# - Project name: igbot2025-api (or your choice)
# - Directory: ./ (current directory)
# - Override settings: No
```

**Note the backend URL:** `https://igbot2025-api.vercel.app`

---

### Step 2: Set Backend Environment Variables

```bash
# Add environment variables
vercel env add IG_ACCOUNTS production
# Enter: username:password:2fa_secret

vercel env add DASHBOARD_USERNAME production
# Enter: admin

vercel env add DASHBOARD_PASSWORD production
# Enter: your_secure_password

# Redeploy to apply env vars
vercel --prod
```

---

### Step 3: Deploy Frontend (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Deploy frontend
vercel --prod

# When prompted:
# - Set up and deploy: Yes
# - Project name: igbot2025-frontend (or your choice)
# - Directory: ./ (current directory)
# - Override settings: No
```

---

### Step 4: Configure Frontend to Connect to Backend

```bash
# Still in frontend directory
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://igbot2025-api.vercel.app (your backend URL from Step 1)

# Redeploy frontend to apply env var
vercel --prod
```

---

## ✅ Verification

After deployment:

### Test Backend
```bash
curl https://your-backend-url.vercel.app/health
# Should return: {"status":"healthy"}
```

### Test Frontend
Open in browser: `https://your-frontend-url.vercel.app`

---

## 🔄 Updated Scripts

I've updated the deployment scripts to handle this correctly:

### Use the Fixed Deploy Script

```bash
./scripts/deploy-all.sh
```

This script now:
1. ✅ Deploys backend from root
2. ✅ Gets backend URL
3. ✅ Sets backend env vars
4. ✅ Deploys frontend from frontend/
5. ✅ Connects frontend to backend
6. ✅ Verifies both deployments

---

## 📋 Quick Commands

### Backend Only
```bash
# From project root
vercel --prod
```

### Frontend Only
```bash
# From frontend directory
cd frontend
vercel --prod
```

### Both (Automated)
```bash
# From project root
./scripts/deploy-all.sh
```

---

## 🐛 Common Issues

### Issue: Frontend can't find backend

**Solution:** Set NEXT_PUBLIC_API_URL in frontend
```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
# Enter your backend URL
vercel --prod
```

### Issue: Backend missing environment variables

**Solution:** Add them to backend project
```bash
# From project root (not frontend/)
vercel env add IG_ACCOUNTS production
vercel env add DASHBOARD_USERNAME production
vercel env add DASHBOARD_PASSWORD production
vercel --prod
```

### Issue: Wrong project when deploying

**Solution:** Link to correct project
```bash
vercel link
# Select the correct project
```

---

## 📊 Project Structure

```
Vercel Dashboard:
├── Project 1: igbot2025-api (Backend)
│   ├── Source: Root directory
│   ├── Framework: Python
│   └── Env Vars: IG_ACCOUNTS, DASHBOARD_USERNAME, etc.
│
└── Project 2: igbot2025-frontend (Frontend)
    ├── Source: frontend/
    ├── Framework: Next.js
    └── Env Vars: NEXT_PUBLIC_API_URL
```

---

## 🎯 Recommended Approach

**Use the automated script:**
```bash
./scripts/deploy-all.sh
```

It handles:
- ✅ Deploying to correct directories
- ✅ Setting environment variables
- ✅ Connecting frontend to backend
- ✅ Health checks
- ✅ Error handling

---

## 📝 Manual Step-by-Step (If Script Doesn't Work)

### Deploy Backend
```bash
# 1. From project root
cd /path/to/igbot2025-1

# 2. Deploy
vercel --prod

# 3. Note the URL (e.g., https://igbot2025-api.vercel.app)

# 4. Add env vars
vercel env add IG_ACCOUNTS production
vercel env add DASHBOARD_USERNAME production
vercel env add DASHBOARD_PASSWORD production

# 5. Redeploy
vercel --prod
```

### Deploy Frontend
```bash
# 1. Go to frontend
cd frontend

# 2. Deploy
vercel --prod

# 3. Add backend URL
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://igbot2025-api.vercel.app

# 4. Redeploy
vercel --prod
```

---

## 🔐 Environment Variables Checklist

### Backend (Root Project)
- [ ] IG_ACCOUNTS
- [ ] DASHBOARD_USERNAME
- [ ] DASHBOARD_PASSWORD
- [ ] MAX_FOLLOWS_PER_DAY (optional)
- [ ] MAX_LIKES_PER_DAY (optional)
- [ ] TIMEZONE (optional)

### Frontend (Frontend Project)
- [ ] NEXT_PUBLIC_API_URL (Backend URL)

---

## 🚀 After Successful Deployment

You'll have two URLs:

**Backend API:**
```
https://your-backend.vercel.app
├── /health - Health check
├── /docs - API documentation
├── /api/status - Bot status
└── /api/analytics - Analytics
```

**Frontend Dashboard:**
```
https://your-frontend.vercel.app
├── / - Home page
├── /login - Login
└── /dashboard - Dashboard
```

---

## 💡 Pro Tips

1. **Keep URLs handy** - Save both deployment URLs
2. **Use separate terminals** - One for backend, one for frontend
3. **Check logs separately** - `vercel logs` in each directory
4. **Link projects** - Use `vercel link` to avoid confusion
5. **Test after deploy** - Always verify both work

---

## 📞 Need Help?

If you get errors:

1. Check you're in the right directory
2. Verify environment variables are set
3. Check logs: `vercel logs`
4. Re-run deployment: `vercel --prod`
5. Use the automated script: `./scripts/deploy-all.sh`

---

**The automated script handles all of this for you!**

```bash
./scripts/deploy-all.sh
```

---

*This fix ensures backend and frontend deploy correctly as separate projects.*
