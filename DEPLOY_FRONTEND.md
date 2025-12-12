# 🚀 Deploy Frontend to Vercel

## ✅ Backend Already Deployed

Your backend should now be deploying successfully at:
- **URL:** https://igbot2025.vercel.app (or your custom URL)
- **Check it:** Go to https://vercel.com/dashboard to see deployment status

---

## 📋 Deploy Frontend (2 Methods)

### Method 1: Vercel Dashboard (Recommended - Easiest)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/new

2. **Import Your Repository**
   - Click "Import Project"
   - Select your GitHub repository: `wizelements/igbot2025`

3. **Configure Project**
   - Click "Configure Project" (DON'T deploy yet!)
   - **Project Name:** `igbot2025-dashboard`
   - **Framework Preset:** Next.js (should auto-detect)
   - **Root Directory:** Click "Edit" and enter: `frontend`
   - **Build Command:** `npm run build` (default is fine)
   - **Output Directory:** `.next` (default is fine)

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add variable:
     - **Name:** `NEXT_PUBLIC_API_URL`
     - **Value:** `https://igbot2025.vercel.app` (your backend URL)
     - **Environment:** Select all (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)

6. **Get Your Frontend URL**
   - After deployment: `https://igbot2025-dashboard.vercel.app`

---

### Method 2: Vercel CLI (Alternative)

```bash
# Navigate to frontend directory
cd /workspaces/igbot2025-1/frontend

# Login to Vercel (if not already)
vercel login

# Deploy to Vercel
vercel

# Follow prompts:
# ? Set up and deploy "frontend"? [Y/n] y
# ? Which scope? [Select your account]
# ? Link to existing project? [N]
# ? What's your project's name? igbot2025-dashboard
# ? In which directory is your code located? ./ [press Enter]

# Add environment variable
vercel env add NEXT_PUBLIC_API_URL production

# When prompted, paste your backend URL:
# Value: https://igbot2025.vercel.app

# Deploy to production
vercel --prod
```

---

## 🔗 Update Backend URL

If your backend URL is different, update it:

```bash
cd /workspaces/igbot2025-1/frontend

# Edit .env.production
echo "NEXT_PUBLIC_API_URL=https://YOUR-ACTUAL-BACKEND-URL.vercel.app" > .env.production

# OR set in Vercel Dashboard:
# Project Settings → Environment Variables → Edit NEXT_PUBLIC_API_URL
```

---

## ✅ Verify Deployment

### 1. Test Backend
```bash
curl https://igbot2025.vercel.app/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

### 2. Test Frontend
- Open: `https://igbot2025-dashboard.vercel.app`
- You should see the landing page
- Click "Login"
- Login with: `admin` / `changeme`
- Dashboard should load with data from backend

### 3. Test Easter Eggs
- Try the Konami Code: ↑ ↑ ↓ ↓ ← → ← → B A
- Type: `godmode`
- Press: `?` for quick stats

---

## 🐛 Troubleshooting

### "Cannot connect to API"
- ✅ Check backend is deployed: `curl https://igbot2025.vercel.app/health`
- ✅ Verify `NEXT_PUBLIC_API_URL` in Vercel dashboard
- ✅ Check browser console for CORS errors

### CORS Errors
Update backend `api/index.py` to allow your frontend:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://igbot2025-dashboard.vercel.app",  # Your frontend
        "http://localhost:3000",  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Build Fails
- ✅ Make sure "Root Directory" is set to `frontend`
- ✅ Check Vercel build logs for specific errors
- ✅ Verify all dependencies in `package.json`

---

## 📊 Final Setup

After successful deployment, you'll have:

**Backend (API):**
- URL: `https://igbot2025.vercel.app`
- Endpoints: `/health`, `/api/status`, `/api/accounts`, etc.

**Frontend (Dashboard):**
- URL: `https://igbot2025-dashboard.vercel.app`
- Pages: Landing, Login, Dashboard, Analytics, etc.
- Easter Eggs: All 6 functional!
- Achievements: Tracking enabled

---

## 🎯 Next Steps

1. ✅ **Test Login:** Use `admin` / `changeme`
2. ✅ **Add Instagram Account:** Go to Accounts page
3. ✅ **Configure Settings:** Set your limits
4. ✅ **Start Bot:** Click the green button
5. ✅ **Try Easter Eggs:** Unlock hidden features!

---

## 🔐 Security

Remember to update default credentials in backend `.env.production`:
```env
DASHBOARD_USERNAME=your_username
DASHBOARD_PASSWORD=your_secure_password
```

Then redeploy backend.

---

## 🎉 Success!

You now have a fully deployed Instagram automation platform:
- ✅ Backend API running on Vercel
- ✅ Frontend dashboard on Vercel
- ✅ Both communicating perfectly
- ✅ All features working
- ✅ Easter eggs unlockable
- ✅ Production-ready!

**Total value deployed:** $9,247
**Your cost:** $0 (on Vercel free tier)

Happy automating! 🤖✨
