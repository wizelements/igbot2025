# Vercel Deployment Quick Start

## 🚀 One-Command Deployment

### Step 1: Verify Everything is Ready

```bash
# Check Next.js is installed
cd /workspaces/igbot2025/frontend
ls package.json  # Should show Next.js
npm list next    # Should show next@14.2.0

# Build to verify it works
npm run build    # Should complete without errors
```

### Step 2: Deploy with Vercel CLI

```bash
# From frontend directory
cd /workspaces/igbot2025/frontend

# Login to Vercel (interactive)
vercel login

# Deploy to production
vercel --prod
```

**You'll be asked:**
```
? Set up and deploy "/workspaces/igbot2025/frontend"? [Y/n] 
→ Answer: y

? Which scope do you want to deploy to? 
→ Select your Vercel account

? Link to existing project? [y/N] 
→ Answer: n (for first deployment)

? What's your project's name? 
→ Enter: igbot-dashboard

? In which directory is your code located? [.]
→ Answer: . (or press Enter)

? Want to modify these settings? [y/N]
→ Answer: n
```

### Step 3: Done! ✅

Your app will be deployed to:
```
https://igbot-dashboard.vercel.app
```

---

## 🔧 Alternative: Deploy via GitHub

### Step 1: Push to GitHub

```bash
cd /workspaces/igbot2025
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 2: Connect in Vercel Dashboard

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Connect your GitHub account
4. Select `igbot2025` repository
5. Click "Import"

### Step 3: Configure

**Root Directory**: Select `/frontend`

**Environment Variables**:
- `NEXT_PUBLIC_API_URL`: `https://your-api.com`

**Build Settings** (auto-detected):
- Framework: Next.js
- Build Command: `npm run build`
- Output Directory: `.next`

### Step 4: Deploy

Click "Deploy" button

---

## 🌍 After Deployment

### Verify It Works

```bash
# Get your deployment URL from Vercel
# Visit: https://your-deployment.vercel.app

# Test in terminal
curl https://your-deployment.vercel.app
# Should return HTML (not error)

# Or open in browser
# Check:
# ✅ Homepage loads
# ✅ Can navigate to /login
# ✅ No 404 errors
# ✅ Styling loads correctly
```

### Configure API Endpoint

If you have a backend API:

1. **In Vercel Dashboard:**
   - Project Settings → Environment Variables
   - Add `NEXT_PUBLIC_API_URL`
   - Set to your backend URL

2. **Redeploy:**
   ```bash
   vercel --prod
   ```

3. **Test Login:**
   - Navigate to `/login`
   - Open DevTools → Network tab
   - Try logging in
   - Verify API calls go to correct endpoint

---

## 🐛 Troubleshooting

### "No Next.js version detected"

**Fix:**
```bash
# Verify Next.js in dependencies
cd /workspaces/igbot2025/frontend
npm list next

# Check package.json has next
grep -A5 '"dependencies"' package.json | grep next

# Reinstall if needed
npm install next@14.2.0
```

### Build Fails

**Check:**
1. `npm run build` works locally?
2. All files committed to git?
3. No missing dependencies?

**Fix:**
```bash
# Clear cache and retry
cd frontend
rm -rf node_modules .next
npm install
npm run build

# Try deployment again
vercel --prod
```

### API Not Connecting

**Check:**
1. Is `NEXT_PUBLIC_API_URL` set in Vercel?
2. Is your API accessible from internet?
3. Does API have CORS headers set?

**Fix:**
```bash
# Add to Vercel environment variables
NEXT_PUBLIC_API_URL=https://your-api.com

# Redeploy
vercel --prod
```

### Page Shows 404

**Fix:**
```bash
# Verify build succeeded
npm run build

# Check output directory
ls -la .next

# Force rebuild
vercel --prod --force
```

---

## 📋 Pre-Deployment Checklist

- ✅ `next` is in `frontend/package.json` dependencies
- ✅ `npm run build` works locally
- ✅ No TypeScript errors: `npm run type-check`
- ✅ No lint errors: `npm run lint`
- ✅ All files committed to git
- ✅ `.env.production` exists and is in `.gitignore`
- ✅ `vercel.json` exists and is valid JSON
- ✅ `.vercelignore` does NOT ignore frontend

### Verify Files Exist

```bash
# Check critical files
ls -la /workspaces/igbot2025/frontend/package.json
ls -la /workspaces/igbot2025/frontend/vercel.json
ls -la /workspaces/igbot2025/vercel.json
ls -la /workspaces/igbot2025/package.json
ls -la /workspaces/igbot2025/.vercelignore
ls -la /workspaces/igbot2025/frontend/.next  # After build
```

---

## 📊 Deployment Command Reference

```bash
# From /workspaces/igbot2025/frontend

# Preview deployment (creates preview URL)
vercel

# Production deployment
vercel --prod

# Show deployment status
vercel list

# View logs
vercel logs

# Rollback to previous version
vercel rollback

# Remove deployment
vercel rm [deployment-id]

# Show current project info
vercel inspect

# Link to existing Vercel project
vercel link
```

---

## 🎯 Success Indicators

After deployment, you should see:

✅ **Vercel Dashboard Shows**
- Green checkmark on deployment
- "Ready" status
- Production domain listed

✅ **Browser Shows**
- IGBot 2025 homepage
- No 404 errors
- Styling loaded correctly
- Can navigate to /login

✅ **Network Tab Shows**
- Initial page load successful
- No failed requests
- Assets loading from Vercel CDN

✅ **Console Shows**
- No critical errors
- Warning about localStorage (normal)

---

## 🚀 Next Steps

1. **Login works?**
   - Test with: `admin` / `changeme`
   - Should redirect to dashboard

2. **Dashboard loads?**
   - Should see stats cards
   - Charts should render
   - No error toasts

3. **API connects?**
   - Set `NEXT_PUBLIC_API_URL` to your backend
   - Click "Start Bot" button
   - Check Network tab for API calls

4. **Custom domain?**
   - Settings → Domains
   - Add your domain
   - Configure DNS records

---

## 📞 Need Help?

See detailed guide: `/VERCEL_DEPLOYMENT.md`
See API docs: `/frontend/lib/README.md`
See fix summary: `/DASHBOARD_FIX_SUMMARY.md`

**Common Issues Doc**: See "Troubleshooting" section in VERCEL_DEPLOYMENT.md

---

## 🎉 Congratulations!

Your IGBot 2025 Dashboard is now live on Vercel! 

**Your app is available at**: `https://your-project.vercel.app`

Share your deployment with:
- Team members
- Stakeholders
- Users

And monitor with Vercel's built-in analytics and error tracking.
