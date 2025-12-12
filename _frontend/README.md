# IGBot 2025 - Frontend Dashboard

🎨 Modern web interface for Instagram automation bot with exclusive Easter eggs!

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🎮 Easter Eggs

This dashboard includes secret features that unlock powerful capabilities:

### 1. **Konami Code** 🎮
Press: `↑ ↑ ↓ ↓ ← → ← → B A`
- Unlocks: Premium Analytics Dashboard
- Shows: Advanced metrics and insights

### 2. **God Mode** 👑
Type: `godmode` (anywhere on the page)
- Unlocks: Advanced bot controls
- Features: Bulk operations, advanced scheduling

### 3. **Time Traveler** ⏰
Click the logo 10 times rapidly
- Unlocks: Historical data viewer
- View: Past performance and trends

### 4. **Matrix Mode** 🟢
Press: `Ctrl + Shift + M`
- Activates: Matrix rain effect
- Toggle on/off

### 5. **Batch Mode** ⚡
Press: `B` key
- Activates: Batch operation shortcuts
- Fast: Multi-account actions

### 6. **Quick Stats** 📊
Press: `?` key
- Shows: Floating stats widget
- Access: Real-time metrics anywhere

## 🏆 Achievement System

Unlock achievements by reaching milestones:

- 👣 **First Steps** - Perform first follow
- 🤝 **Networking Pro** - 100 follows
- ❤️ **Love Spreader** - 1000 likes
- 🔥 **Dedicated** - 7-day streak
- 👑 **Empire Builder** - 5 accounts
- ⭐ **Flawless** - 100% success rate day
- 🌅 **Early Bird** - Start before 6 AM
- 🦉 **Night Owl** - Run past midnight

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── dashboard/         # Dashboard pages
│   ├── login/            # Auth pages
│   ├── globals.css       # Global styles
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/            # Reusable components
│   └── Sidebar.tsx       # Navigation
├── lib/                   # Utilities
│   ├── api.ts           # API client
│   └── easter-eggs.ts   # Easter egg system
└── public/               # Static assets
```

## 🎨 Features

- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Real-time data updates
- ✅ Interactive charts and graphs
- ✅ Dark mode optimized
- ✅ Smooth animations with Framer Motion
- ✅ Toast notifications
- ✅ Protected routes
- ✅ Easter eggs & achievements
- ✅ Batch operations
- ✅ Export reports

## 🔐 Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-api-url.vercel.app
```

## 📦 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Animations**: Framer Motion
- **State**: Zustand
- **Data Fetching**: TanStack Query
- **Icons**: Lucide React
- **Notifications**: React Hot Toast

## 🚀 Deployment

### Vercel (Recommended)

```bash
vercel
```

### Manual

```bash
npm run build
npm start
```

## 💡 Usage Tips

1. **Navigate Fast**: Use keyboard shortcuts
2. **Monitor Real-time**: Enable auto-refresh
3. **Bulk Actions**: Press 'B' for batch mode
4. **Quick Stats**: Press '?' for floating widget
5. **Export Data**: Download reports anytime

## 🐛 Troubleshooting

### API Connection Issues
- Check `.env.local` file
- Verify API URL is correct
- Ensure CORS is enabled on backend

### Easter Eggs Not Working
- Clear browser cache
- Check localStorage
- Verify JavaScript is enabled

## 📝 License

MIT License - Built with ❤️ for IGBot 2025

---

**Happy Automating! 🤖**
