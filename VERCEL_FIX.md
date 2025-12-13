# Vercel Deployment Fix

## Problem
Project `igbot2025-1` has framework preset locked to Next.js, causing deployment failures.

## Solution: Create New Backend Project

### Step 1: Delete Old Backend Project
```bash
# Go to: https://vercel.com/theangelsilvers-projects/igbot2025-1/settings/general
# Scroll down and click "Delete Project"
```

### Step 2: Create New Project via CLI

```bash
cd /workspaces/igbot2025-1
rm -rf .vercel
vercel --prod
```

When prompted:
- **Set up and deploy?** Yes
- **Which scope?** Select your team
- **Link to existing project?** No
- **What's your project's name?** `igbot2025-backend` (or similar)
- **In which directory is your code located?** `./` (root)
- **Want to override the settings?** Yes
- **Build Command:** Leave empty or `echo "Serverless"`
- **Output Directory:** Leave empty
- **Development Command:** Leave empty

### Step 3: Verify Deployment

The deployment should succeed because:
1. Fresh project = no framework preset lock
2. `vercel.json` will be respected
3. Python API will deploy correctly

### Step 4: Update Frontend Environment

Once deployed, update frontend's `NEXT_PUBLIC_API_URL`:
```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://igbot2025-backend.vercel.app (your new backend URL)
vercel --prod
```

## Alternative: Use Vercel Dashboard

1. Go to Vercel Dashboard → Add New → Project
2. Import `wizelements/igbot2025` 
3. **CRITICAL:** Set Framework Preset to "Other" (NOT Next.js)
4. Root Directory: `.`
5. Build Command: Leave empty
6. Deploy

This ensures a clean slate without the Next.js lock.
