# Vercel Deployment Guide - IGBot 2025

Complete guide to deploy IGBot 2025 Dashboard to Vercel.

## Prerequisites

- Vercel account (free at https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)
- Node.js 20.x and npm installed locally
- Vercel CLI installed: `npm install -g vercel`

## Architecture

```
┌─────────────────────────────────────────────────┐
│           Vercel Deployment                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  Frontend (Next.js 14)                   │   │
│  │  /frontend/                              │   │
│  │  • Deployed as default project           │   │
│  │  • Routes: /, /login, /dashboard/*       │   │
│  │  • Size: ~266 KB per page                │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  API Proxy (Optional)                    │   │
│  │  /api/                                   │   │
│  │  • Routes to external backend            │   │
│  │  • Or deploy FastAPI backend             │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Step 1: Prepare Repository

### 1.1 Create Git Repository (if not exists)

```bash
cd /workspaces/igbot2025
git init
git add .
git commit -m "Initial commit - IGBot 2025 with Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/igbot2025.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Project Structure

```bash
ls -la
# Should show:
# - frontend/     ← Next.js app (main deployment)
# - api/          ← FastAPI backend (optional)
# - vercel.json   ← Deployment config
# - package.json  ← Root package.json
```

### 1.3 Check Configuration Files

Required files in place:
- ✅ `/vercel.json` - Deployment configuration
- ✅ `/frontend/vercel.json` - Frontend-specific config
- ✅ `/frontend/package.json` - Has Next.js
- ✅ `/package.json` - Root package.json with build scripts
- ✅ `/frontend/.env.production` - (Keep secrets private)
- ✅ `.vercelignore` - Ignore unnecessary files

## Step 2: Build Locally & Test

### 2.1 Install Dependencies

```bash
cd /workspaces/igbot2025/frontend
npm install
```

### 2.2 Verify Build

```bash
npm run build
```

Expected output:
```
✓ Compiled successfully
✓ Generating static pages (10/10)
Route (app)                    Size     First Load JS
├ ○ /                          3.21 kB  148 kB
├ ○ /login                     2.95 kB  152 kB
├ ○ /dashboard                10.2 kB  266 kB
...
○  (Static) prerendered as static content
```

### 2.3 Test Production Build Locally

```bash
npm run build
npm start
```

Open browser: http://localhost:3000

Verify:
- ✅ Home page loads
- ✅ Can navigate to /login
- ✅ Login form works
- ✅ No errors in console

## Step 3: Configure Vercel Environment

### 3.1 Using Vercel Dashboard

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Select `frontend` as root directory (if prompted)
5. Configure environment variables:
   - `NEXT_PUBLIC_API_URL`: Your API endpoint
   - Add any other required vars

### 3.2 Environment Variables

**Production (.env.production)**
```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NODE_ENV=production
```

**Add to Vercel Dashboard:**
1. Project Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL`
3. Set value based on your backend:
   - If using Vercel's Python runtime: `https://yourapp.vercel.app/api`
   - If using external API: `https://your-api.com`
   - If using Railway/Heroku: `https://your-backend.com`

### 3.3 Build Settings

Vercel should auto-detect:
- Framework: **Next.js**
- Build Command: **`npm run build`**
- Output Directory: **`.next`**
- Install Command: **`npm install`**

If not, manually set in Project Settings:
```
Build Command:     npm run build
Output Directory:  .next
Install Command:   npm install
Node Version:      20.x
```

## Step 4: Deploy Using Vercel CLI

### 4.1 Login to Vercel

```bash
vercel login
# Follow prompts to authenticate
```

### 4.2 First Deployment (From Frontend)

```bash
cd /workspaces/igbot2025/frontend
vercel --prod
```

**Follow prompts:**
```
Set up and deploy "/workspaces/igbot2025/frontend"? [Y/n] y
Which scope do you want to deploy to? [username]
Link to existing project? [y/N] n
What's your project's name? igbot-dashboard
In which directory is your code located? [.] .
Want to modify these settings? [y/N] n
```

**Expected output:**
```
Deploying ~/igbot2025/frontend under [username]
✓ Created project [username]/igbot-dashboard
✓ Linked to [username]/igbot-dashboard
✓ Built Successfully
✓ Deployed to https://igbot-dashboard.vercel.app [v1]
```

### 4.3 Production Deployment (Final)

```bash
cd /workspaces/igbot2025/frontend
vercel --prod
```

This deploys to your production domain.

## Step 5: Verify Deployment

### 5.1 Test Live Deployment

```bash
# Get the deployment URL from Vercel
# Should be something like: https://igbot-dashboard.vercel.app

curl https://igbot-dashboard.vercel.app
# Should return HTML (not error)
```

### 5.2 Verify in Browser

1. Open: https://igbot-dashboard.vercel.app
2. Check:
   - ✅ Page loads without 404
   - ✅ Styling loads (not plain HTML)
   - ✅ No console errors
   - ✅ Can navigate to /login

### 5.3 Test API Connection

If using backend API:

1. Set `NEXT_PUBLIC_API_URL` to your backend
2. Go to /login
3. Try logging in (check Network tab)
4. Verify API calls succeed (200 status)

## Step 6: Configure Custom Domain (Optional)

### 6.1 Add Custom Domain

1. Vercel Dashboard → Project → Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., `igbot.example.com`)
4. Follow DNS configuration steps

### 6.2 Configure DNS

Vercel provides nameservers or DNS records:
```
ALIAS/CNAME: igbot.example.com → cname.vercel-dns.com
```

Verify with:
```bash
nslookup igbot.example.com
dig igbot.example.com
```

## Step 7: Monitor & Maintain

### 7.1 View Deployment Logs

```bash
vercel logs --prod
# or in Vercel Dashboard → Deployments → View Function Logs
```

### 7.2 Check Performance

Vercel Dashboard:
- **Deployments** - View all versions
- **Analytics** - Monitor usage
- **Functions** - Check API endpoints
- **Settings** - Update environment variables

### 7.3 Roll Back Deployment

If issues occur:
```bash
vercel rollback
# Or in Dashboard: Deployments → Click previous version → Promote
```

## Troubleshooting

### Issue: "No Next.js version detected"

**Solution:**
1. Ensure `next` is in `frontend/package.json` dependencies
2. Set root directory to `frontend` in Vercel settings
3. Use `vercel --prod --cwd=frontend`

### Issue: "Cannot find module '@/lib/api'"

**Solution:**
1. Verify files exist:
   ```bash
   ls -la frontend/lib/api.ts
   ls -la frontend/lib/easter-eggs.ts
   ```
2. Commit and push files to git
3. Redeploy

### Issue: API calls return 401 Unauthorized

**Solution:**
1. Check `NEXT_PUBLIC_API_URL` is set correctly
2. Verify backend is running and accessible
3. Check credentials in browser console (Network tab)
4. Verify CORS is enabled on backend

### Issue: Static files not loading (CSS, JS)

**Solution:**
1. Check `.vercelignore` is not excluding critical files
2. Verify `outputDirectory` is `.next` in vercel.json
3. Check for path prefix issues in next.config.js
4. Clear Vercel cache:
   ```bash
   vercel --prod --force
   ```

### Issue: Deployment takes too long or times out

**Solution:**
1. Check `package.json` for unnecessary dependencies
2. Optimize build:
   ```bash
   npm ci --production  # Use ci for production
   ```
3. Enable build caching in Vercel Settings
4. Split large bundles

### Issue: Database/API connection issues

**Solution:**
1. Ensure backend is accessible from Vercel
2. Check firewall rules allow Vercel IPs
3. Verify environment variables are set
4. Check API endpoint URL format

## Advanced Configuration

### Custom Build Script

Create `build.sh`:
```bash
#!/bin/bash
cd frontend
npm install
npm run build
```

Then in `vercel.json`:
```json
{
  "buildCommand": "./build.sh"
}
```

### Serverless Functions

If deploying Python API to Vercel:

```json
{
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next@latest"
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend"
    }
  ]
}
```

### Environment-Specific Builds

Preview deployments automatically use `.env.preview`:
```
NEXT_PUBLIC_API_URL=https://preview-api.example.com
```

Production uses `.env.production`:
```
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use Vercel's encrypted environment variables
3. ✅ Enable HTTPS (automatic)
4. ✅ Set proper CORS headers
5. ✅ Validate all API inputs
6. ✅ Use secure tokens/API keys
7. ✅ Monitor deployment logs for errors
8. ✅ Keep dependencies updated

## Performance Optimization

1. **Image Optimization**
   - Use `next/image` component
   - Vercel auto-optimizes images

2. **Code Splitting**
   - Next.js auto-splits code
   - Lazy load heavy components

3. **Caching**
   - Set proper Cache-Control headers
   - Use vercel.json routes for caching

4. **Monitoring**
   - Enable Vercel Analytics
   - Monitor Core Web Vitals

## Post-Deployment Checklist

- ✅ Domain configured and accessible
- ✅ Environment variables set
- ✅ API connection working
- ✅ Login functionality tested
- ✅ Dashboard loads with data
- ✅ Mobile responsive
- ✅ No console errors
- ✅ Performance metrics acceptable
- ✅ Monitoring enabled
- ✅ Backup and rollback procedures ready

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Vercel CLI**: https://vercel.com/cli
- **Community**: https://vercel.com/support

## Deployment History

| Date | Version | Status | URL |
|------|---------|--------|-----|
| 2025-12-18 | 1.0.0 | Ready | https://igbot-dashboard.vercel.app |

---

For issues or questions, check `/frontend/lib/README.md` or `/DASHBOARD_FIX_SUMMARY.md`
