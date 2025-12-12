# Install Vercel CLI First

Before running `./scripts/deploy-all.sh`, you need to install and setup Vercel CLI.

---

## Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

**If you don't have Node.js/npm installed:**

### Ubuntu/Debian:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### macOS:
```bash
brew install node
```

### Windows:
Download from https://nodejs.org/

---

## Step 2: Login to Vercel

```bash
vercel login
```

This will:
1. Open your browser
2. Ask you to sign in (or create a free account at https://vercel.com)
3. Authorize the CLI

---

## Step 3: Run Deployment Script

```bash
./scripts/deploy-all.sh
```

The script will guide you through deploying both backend and frontend.

---

## Alternative: Quick Manual Deployment

### Deploy Backend
```bash
vercel --prod
```

### Deploy Frontend
```bash
cd frontend
vercel --prod
```

---

## Verify Installation

Check if Vercel is installed:
```bash
vercel --version
```

Check if you're logged in:
```bash
vercel whoami
```

---

## Complete Quick Start

```bash
# 1. Install
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
./scripts/deploy-all.sh
```

That's it! 🚀
