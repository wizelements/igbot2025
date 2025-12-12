# 🎨 IGBot 2025 - Web Interface Setup Guide

Complete guide to set up and deploy the exclusive web interface for IGBot 2025.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Easter Eggs & Features](#easter-eggs--features)
4. [Deployment](#deployment)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Your IGBot API running (backend)
- Git

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local with your API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

**Default Login:**
- Username: `admin`
- Password: `changeme`

---

## 💻 Local Development

### Development Server

```bash
cd frontend
npm run dev
```

Access at: `http://localhost:3000`

### Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Landing page
│   ├── login/page.tsx        # Login page
│   ├── dashboard/            # Dashboard routes
│   │   ├── page.tsx         # Main dashboard
│   │   ├── accounts/        # Account management
│   │   ├── analytics/       # Analytics & charts
│   │   └── layout.tsx       # Dashboard layout
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── providers.tsx        # React Query provider
│
├── components/
│   └── Sidebar.tsx          # Navigation sidebar
│
├── lib/
│   ├── api.ts              # API client
│   └── easter-eggs.ts      # Easter egg system
│
└── public/                  # Static files
```

### Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

---

## 🎮 Easter Eggs & Features

### 1. Konami Code 🎮

**How to activate:** Press `↑ ↑ ↓ ↓ ← → ← → B A`

**Unlocks:**
- Premium Analytics Dashboard
- Advanced metrics visualization
- Detailed performance insights
- Predictive analytics

**Value:** See deeper insights into bot performance with ML-powered predictions.

---

### 2. God Mode 👑

**How to activate:** Type `godmode` anywhere on the page

**Unlocks:**
- Advanced bot controls
- Bulk operations panel
- Custom scheduling interface
- Override safety limits (use carefully!)

**Value:** Professional-grade controls for power users.

---

### 3. Time Traveler ⏰

**How to activate:** Click the IGBot logo 10 times rapidly

**Unlocks:**
- Historical data viewer
- Time-series analysis
- Trend predictions
- Performance comparisons

**Value:** Understand growth patterns over time.

---

### 4. Matrix Mode 🟢

**How to activate:** Press `Ctrl + Shift + M`

**Unlocks:**
- Matrix rain visual effect
- Hacker aesthetic
- Toggle on/off

**Value:** Cool visual effect while monitoring bots.

---

### 5. Batch Mode ⚡

**How to activate:** Press `B` key

**Unlocks:**
- Multi-account selection
- Bulk action execution
- Quick operation toolbar
- Time-saving shortcuts

**Value:** Manage multiple accounts simultaneously.

---

### 6. Quick Stats Widget 📊

**How to activate:** Press `?` key

**Unlocks:**
- Floating stats panel
- Real-time metrics
- Follows you across pages

**Value:** Monitor key metrics without switching views.

---

### 7. Achievement System 🏆

Automatically tracks and rewards milestones:

| Achievement | Requirement | Reward |
|------------|-------------|--------|
| 👣 First Steps | First follow action | Welcome bonus |
| 🤝 Networking Pro | 100 follows | Efficiency tips |
| ❤️ Love Spreader | 1000 likes | Engagement insights |
| 🔥 Dedicated | 7-day streak | Premium tips |
| 👑 Empire Builder | 5 accounts | Multi-account guide |
| ⭐ Flawless | 100% success day | Best practices |
| 🌅 Early Bird | Start before 6 AM | Peak time insights |
| 🦉 Night Owl | Run past midnight | Night strategy |

**Value:** Gamification encourages best practices and exploration.

---

## 🚀 Deployment

### Option 1: Vercel (Recommended)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Set build command: npm run build
# - Set output directory: .next
# - Add environment variable: NEXT_PUBLIC_API_URL
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your backend API URL

### Option 2: Netlify

```bash
cd frontend

# Build
npm run build

# Deploy to Netlify
# Upload the 'out' folder
```

Configure in Netlify:
- Build command: `npm run build`
- Publish directory: `out`
- Environment: `NEXT_PUBLIC_API_URL`

### Option 3: Docker

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```bash
docker build -t igbot-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=https://your-api.com igbot-frontend
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-api.vercel.app

# Optional: Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_ACHIEVEMENTS=true
```

### API Integration

Update `lib/api.ts` if needed:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

### Authentication

Default credentials are stored in backend. To change:

1. Update backend environment variables:
   ```
   DASHBOARD_USERNAME=your_username
   DASHBOARD_PASSWORD=your_secure_password
   ```

2. No frontend changes needed (uses Basic Auth)

---

## 🎨 Customization

### Change Theme Colors

Edit `tailwind.config.ts`:

```typescript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
        500: '#your-color',
      },
    },
  },
}
```

### Add Custom Features

1. Create new component in `components/`
2. Add route in `app/dashboard/`
3. Update sidebar in `components/Sidebar.tsx`

### Modify Easter Eggs

Edit `lib/easter-eggs.ts`:

```typescript
// Add new easter egg
private myCustomEgg = 'secret'

public onCustomUnlock?: () => void
```

---

## 🐛 Troubleshooting

### Issue: Cannot connect to API

**Solution:**
```bash
# Check .env.local
cat .env.local

# Verify API is running
curl http://localhost:8000/health

# Check CORS settings in backend
```

### Issue: Easter eggs not working

**Solution:**
```bash
# Clear localStorage
localStorage.clear()

# Check browser console for errors
# Ensure JavaScript is enabled
```

### Issue: Build fails

**Solution:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+

# Try build again
npm run build
```

### Issue: Slow performance

**Solution:**
```bash
# Enable production mode
npm run build
npm start

# Check React Query cache settings
# Reduce refetch intervals
```

---

## 📊 Performance Optimization

### 1. Enable Production Build

```bash
npm run build
npm start
```

### 2. Configure Caching

Update `lib/api.ts`:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      cacheTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})
```

### 3. Optimize Images

Place images in `public/` and use Next.js Image:

```tsx
import Image from 'next/image'

<Image src="/logo.png" width={200} height={200} alt="Logo" />
```

---

## 🔐 Security Best Practices

1. **Never commit `.env.local`**
2. **Use strong passwords**
3. **Enable HTTPS in production**
4. **Implement rate limiting**
5. **Regular dependency updates**

```bash
# Check for vulnerabilities
npm audit

# Fix automatically
npm audit fix
```

---

## 📱 Mobile Optimization

The interface is fully responsive. Test on mobile:

```bash
# Access from mobile device
# Find your local IP
ifconfig | grep "inet "

# Access at: http://YOUR_IP:3000
```

---

## 🎓 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Guide](https://tanstack.com/query)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)

---

## 🤝 Contributing

To add features:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📞 Support

Issues? Questions?

1. Check troubleshooting section
2. Review API logs
3. Check browser console
4. Review GitHub issues

---

## 🎉 Success Checklist

- [ ] Frontend installed and running
- [ ] Connected to backend API
- [ ] Login working
- [ ] Dashboard displaying data
- [ ] All pages accessible
- [ ] Easter eggs tested
- [ ] Achievements tracking
- [ ] Deployed to production
- [ ] SSL certificate configured
- [ ] Environment variables set

---

**Built with ❤️ for IGBot 2025**

Enjoy the exclusive web interface! 🚀
