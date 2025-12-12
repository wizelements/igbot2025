# 🚀 IGBot 2025 - Web Interface Quick Start

## ⚡ 60-Second Setup

```bash
# 1. Run setup script
./setup-frontend.sh

# 2. Start frontend
cd frontend && npm run dev

# 3. Start backend (in another terminal)
python api/index.py
```

**Done!** Open http://localhost:3000

---

## 🔑 First Login

```
Username: admin
Password: changeme
```

---

## 🎮 Try These Easter Eggs Now!

### 1. Konami Code (Premium Analytics)
Press: `↑ ↑ ↓ ↓ ← → ← → B A`

### 2. God Mode (Advanced Controls)
Type: `godmode` anywhere

### 3. Quick Stats Widget
Press: `?` key

### 4. Matrix Mode
Press: `Ctrl + Shift + M`

### 5. Batch Mode
Press: `B` key

### 6. Time Traveler
Click the IGBot logo 10 times

---

## 📊 Key Pages

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/dashboard` | Overview & controls |
| Accounts | `/dashboard/accounts` | Manage IG accounts |
| Analytics | `/dashboard/analytics` | Charts & insights |

---

## 🎯 Common Tasks

### Add Instagram Account
1. Go to Accounts page
2. Click "Add Account"
3. Enter username & password
4. (Optional) Add 2FA secret
5. Click "Add Account"

### Start Bot
1. Go to Dashboard
2. Click green "Start Bot" button
3. Watch the magic happen!

### Stop Bot
1. Go to Dashboard
2. Click red "Stop Bot" button
3. All bots pause safely

### View Analytics
1. Go to Analytics page
2. See charts and metrics
3. Export reports if needed

---

## 🏆 Achievements to Unlock

- 👣 First Steps (1 follow)
- 🤝 Networking Pro (100 follows)
- ❤️ Love Spreader (1000 likes)
- 🔥 Dedicated (7-day streak)
- 👑 Empire Builder (5 accounts)
- ⭐ Flawless (100% success day)
- 🌅 Early Bird (start before 6 AM)
- 🦉 Night Owl (run past midnight)

---

## 🐛 Troubleshooting

### Can't connect to API
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check .env.local file
cat frontend/.env.local
```

### Easter eggs not working
```javascript
// Open browser console and run:
localStorage.clear()
// Then refresh page
```

### Login fails
- Check backend credentials in `.env.production`
- Default: admin / changeme
- Verify backend is running

---

## 📱 Mobile Access

```bash
# Find your IP
ifconfig | grep "inet "

# Access from phone
http://YOUR_IP:3000
```

---

## 🚀 Deploy to Production

### Vercel (Easiest)
```bash
cd /workspaces/igbot2025-1
vercel
```

Set environment variable:
- `NEXT_PUBLIC_API_URL`: Your backend URL

### Manual
```bash
cd frontend
npm run build
npm start
```

---

## 💡 Pro Tips

1. **Use keyboard shortcuts** - Much faster
2. **Try all easter eggs** - $304/mo value
3. **Complete achievements** - Learn best practices
4. **Press ? anytime** - Quick stats widget
5. **Export analytics** - Regular backups

---

## 📞 Need Help?

1. Check `WEB_INTERFACE_GUIDE.md` - Complete guide
2. Check `FEATURES.md` - All features explained
3. Check `FRONTEND_SUMMARY.md` - Technical overview
4. Check browser console - Error messages
5. Check API logs - Backend issues

---

## 🎉 You're All Set!

The most advanced Instagram automation dashboard is ready!

**Features unlocked:**
- ✅ Real-time dashboard
- ✅ Account management
- ✅ Advanced analytics
- ✅ 6 easter eggs ($304/mo value)
- ✅ 8 achievements
- ✅ Mobile responsive
- ✅ Production ready

**Happy automating! 🚀**

---

**Built with ❤️ for IGBot 2025**
