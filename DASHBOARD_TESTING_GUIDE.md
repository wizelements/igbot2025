# Dashboard Testing Guide

## Pre-Testing Setup

### 1. Backend Server

Start the FastAPI backend server:

```bash
# From root directory
cd api
pip install -r requirements.txt
python -m uvicorn index:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Test backend is working:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-18T...",
  "version": "1.0.0",
  "environment": "production"
}
```

### 2. Frontend Development Server

Start the Next.js development server:

```bash
cd frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 14.2.35
  - Ready in 2.1s
  - Local:        http://localhost:3000
```

---

## Testing Scenarios

### Test 1: Build Compilation

**Objective**: Verify frontend builds without errors

**Steps**:
```bash
cd frontend
npm run build
```

**Expected Result**:
```
✓ Compiled successfully
✓ Linting passed
✓ 8 pages generated
✓ Build time: ~30 seconds
```

**Success Criteria**:
- ✅ No "module not found" errors
- ✅ No TypeScript compilation errors
- ✅ No ESLint warnings
- ✅ Build output shows all 8 pages

---

### Test 2: Dev Server Startup

**Objective**: Verify dev server starts and serves pages

**Steps**:
```bash
cd frontend
npm run dev
```

Wait for startup to complete (~2 seconds)

**Expected Result**:
```
✓ Ready in 2.1s
✓ Listening on http://localhost:3000
```

**Success Criteria**:
- ✅ Server starts without errors
- ✅ No console warnings about missing modules
- ✅ Available on http://localhost:3000

---

### Test 3: Login Page

**Objective**: Verify login page renders and authenticates

**Steps**:
1. Open browser: `http://localhost:3000/login`
2. Verify page loads with:
   - Login form visible
   - Username field
   - Password field
   - Sign In button
   - Default credentials hint (admin/changeme)

3. Enter credentials:
   - Username: `admin`
   - Password: `changeme`

4. Click "Sign In"

**Expected Result**:
- ✅ Page loads without errors
- ✅ Form is interactive
- ✅ Submit button works
- ✅ Success toast appears: "Welcome back! 🎉"
- ✅ Redirects to `/dashboard`
- ✅ No 401 errors in console

**Failure Handling**:
- ❌ If 401 error: Check backend is running and credentials are correct
- ❌ If page doesn't load: Check backend API URL in `.env.production`
- ❌ If form doesn't submit: Check browser console for errors

---

### Test 4: Dashboard Page

**Objective**: Verify dashboard loads and fetches live data

**Prerequisite**: Must be logged in from Test 3

**Steps**:
1. Navigate to `http://localhost:3000/dashboard`
2. Verify page elements:
   - Header with "Dashboard" title
   - Start/Stop Bot buttons
   - 4 stat cards (Accounts, Actions, Success Rate, Status)
   - Two charts (Activity, Actions Breakdown)
   - Account Status section
   - Quick Tip section

3. Verify data is loading:
   - Stat cards show numbers (may be 0 initially)
   - Charts render with mock data
   - No error messages

**Expected Result**:
- ✅ Page renders completely
- ✅ All components visible
- ✅ Data displays in stat cards
- ✅ Charts render properly
- ✅ No console errors
- ✅ Network tab shows successful API calls:
  - GET /api/status (200)
  - GET /api/accounts (200)
  - GET /api/analytics (200)

**Failure Handling**:
- ❌ If stat cards show 0: Backend may not have data, normal
- ❌ If charts don't render: Check recharts is loaded
- ❌ If API calls fail: Check backend API URL and credentials

---

### Test 5: Bot Control (Start/Stop)

**Objective**: Verify Start/Stop Bot buttons function

**Prerequisite**: Must be on dashboard page

**Steps**:
1. Click "Start Bot" button
2. Verify:
   - Button shows loading spinner
   - Success toast appears: "🚀 Bot started successfully!"
   - Button returns to normal state
   - Check network tab for POST to `/api/bot/start`

3. Click "Stop Bot" button
4. Verify:
   - Button shows loading spinner
   - Success toast appears: "⏸️ Bot stopped successfully!"
   - Button returns to normal state
   - Check network tab for POST to `/api/bot/stop`

**Expected Result**:
- ✅ Both buttons respond immediately
- ✅ Loading states display correctly
- ✅ Success toasts appear
- ✅ API calls complete successfully
- ✅ No error messages

**Failure Handling**:
- ❌ If buttons don't respond: Check browser console
- ❌ If API calls fail: Verify backend is running
- ❌ If no toast appears: Check react-hot-toast initialization

---

### Test 6: Accounts Page

**Objective**: Verify accounts management page

**Steps**:
1. Navigate to `/dashboard/accounts`
2. Verify page loads with:
   - "Accounts" title
   - "Add Account" button
   - Account cards (if any exist)
   - Each account shows: username, status, actions count

3. Click "Add Account" button
4. Verify modal opens with:
   - Username field
   - Password field
   - 2FA Secret field (optional)
   - Cancel and Add buttons

5. Fill in test account:
   - Username: `test_account`
   - Password: `test_password`
   - Leave 2FA blank

6. Click "Add Account"
7. Verify:
   - Modal closes
   - Success toast appears
   - Account list updates

**Expected Result**:
- ✅ Page loads without errors
- ✅ Modal opens and closes properly
- ✅ Form validation works
- ✅ API call succeeds (200)
- ✅ Toast notifications appear

**Failure Handling**:
- ❌ If modal doesn't open: Check framer-motion is loaded
- ❌ If form doesn't submit: Check console for validation errors
- ❌ If API fails: Verify backend and CORS config

---

### Test 7: Analytics Page

**Objective**: Verify analytics and metrics display

**Steps**:
1. Navigate to `/dashboard/analytics`
2. Verify page loads with:
   - Analytics title
   - Metrics cards (success rate, action count, etc.)
   - Charts displaying data trends
   - Account breakdown section

3. Wait 30 seconds
4. Verify data updates (due to 30s refetch interval)

**Expected Result**:
- ✅ Page renders completely
- ✅ Charts display properly
- ✅ Data updates periodically
- ✅ No console errors
- ✅ API calls occur every 30 seconds

**Failure Handling**:
- ❌ If charts don't render: Check recharts installation
- ❌ If data doesn't update: Check React Query refetch settings

---

### Test 8: Sidebar Navigation

**Objective**: Verify sidebar navigation works

**Steps**:
1. From dashboard, click "Accounts" in sidebar
2. Verify navigation to `/dashboard/accounts`
3. Click "Analytics" in sidebar
4. Verify navigation to `/dashboard/analytics`
5. Click "Actions" in sidebar
6. Verify navigation to `/dashboard/actions`
7. Click "Settings" in sidebar
8. Verify navigation to `/dashboard/settings`
9. Click "Logout" button
10. Verify redirect to `/login`

**Expected Result**:
- ✅ All navigation links work
- ✅ Pages load without errors
- ✅ Logout clears session
- ✅ Cannot access dashboard after logout
- ✅ Redirected to login page

**Failure Handling**:
- ❌ If navigation fails: Check routing in Next.js
- ❌ If logout doesn't work: Check auth.logout() implementation

---

### Test 9: Authentication Persistence

**Objective**: Verify login session persists

**Steps**:
1. Login with admin/changeme
2. Open browser dev tools > Application > Storage > localStorage
3. Verify `auth_credentials` key exists with JSON value
4. Refresh the page (Ctrl+R)
5. Verify dashboard loads immediately without redirect to login
6. Clear localStorage
7. Refresh page
8. Verify redirected to login page

**Expected Result**:
- ✅ Credentials stored in localStorage
- ✅ Persists across page refreshes
- ✅ Automatically logs in after refresh
- ✅ Clearing storage requires re-login

**Failure Handling**:
- ❌ If localStorage empty: Check auth.login() saves credentials
- ❌ If session doesn't persist: Check useEffect in layout.tsx

---

### Test 10: Easter Eggs - Konami Code

**Objective**: Verify Konami code detection

**Steps**:
1. Be on any dashboard page
2. Press the Konami code sequence:
   - **Up Arrow** (↑)
   - **Up Arrow** (↑)
   - **Down Arrow** (↓)
   - **Down Arrow** (↓)
   - **Left Arrow** (←)
   - **Right Arrow** (→)
   - **Left Arrow** (←)
   - **Right Arrow** (→)
   - **B** key
   - **A** key

3. Verify:
   - Toast appears: "🎮 Premium Analytics Unlocked!"
   - Achievement notification appears
   - Sidebar shows "Premium Analytics" menu item (yellow border)

4. Check localStorage:
   - Dev Tools > Application > Storage > localStorage
   - Key: `easter_eggs_unlocked`
   - Should contain: `["konami"]`

**Expected Result**:
- ✅ Code sequence recognized
- ✅ Toast notification appears
- ✅ Achievement event fires
- ✅ Feature unlocked in localStorage
- ✅ Premium menu item appears

**Failure Handling**:
- ❌ If code not detected: Check keyboard event listeners
- ❌ If toast doesn't appear: Check callback is set in layout.tsx
- ❌ If menu doesn't appear: Check easterEggs.isUnlocked() in sidebar

---

### Test 11: Easter Eggs - Logo Clicks

**Objective**: Verify logo click unlocks

**Steps**:
1. On dashboard, find the IGBot logo in the sidebar
2. **Test 1: Click 5 times**
   - Rapid click 5 times on logo
   - Verify toast: "Achievement Unlocked"
   - Check localStorage for `"god-mode"`

3. **Test 2: Click 10 more times** (5 more clicks total)
   - Rapid click 10 more times
   - Verify new achievement toast
   - Check localStorage for `"time-traveler"`

4. **Test 3: Click 5 more times** (5 more total)
   - Rapid click 5 more times
   - Verify matrix mode achievement
   - Check localStorage for `"matrix"`

**Expected Result**:
- ✅ 5+ clicks → god-mode unlocked
- ✅ 10+ clicks → time-traveler unlocked
- ✅ 15+ clicks → matrix unlocked
- ✅ Features visible in localStorage
- ✅ Achievement notifications appear

**Failure Handling**:
- ❌ If clicks not detected: Check handleLogoClick() in sidebar
- ❌ If achievements don't unlock: Check logo click tracking
- ❌ If toasts don't appear: Check callback handlers in layout.tsx

---

### Test 12: Quick Stats (? key)

**Objective**: Verify quick stats widget

**Steps**:
1. On dashboard, press **?** key (Shift+/)
2. Verify:
   - Widget appears in top-right corner
   - Shows: Active accounts, Today's actions, Success rate
   - Has close button (X)

3. Press **?** again
4. Verify widget disappears

5. Press **?** again
6. Verify widget re-appears

**Expected Result**:
- ✅ Widget toggles on/off with ? key
- ✅ Displays stats correctly
- ✅ Close button works
- ✅ Smooth animation on appear/disappear

**Failure Handling**:
- ❌ If widget doesn't appear: Check keyboard listener in easter-eggs.ts
- ❌ If animation stutters: Check Framer Motion setup
- ❌ If close button doesn't work: Check button onClick handler

---

### Test 13: Error Handling - Invalid Credentials

**Objective**: Verify error handling for auth failures

**Steps**:
1. Go to `/login`
2. Enter wrong credentials:
   - Username: `admin`
   - Password: `wrongpassword`
3. Click "Sign In"
4. Verify:
   - Toast error appears: "Invalid credentials..."
   - Remains on login page
   - Form is not cleared (preserved for editing)

5. Check network tab:
   - Request shows Basic Auth header
   - Response status is 401 Unauthorized

**Expected Result**:
- ✅ Error toast appears immediately
- ✅ Not redirected away
- ✅ Can retry with correct credentials
- ✅ No sensitive info in console

**Failure Handling**:
- ❌ If accepted wrong credentials: Check backend validation
- ❌ If no error message: Check error handling in login page
- ❌ If redirects anyway: Check condition in handleLogin()

---

### Test 14: Auto-Logout on 401

**Objective**: Verify auto-logout when session expires

**Steps**:
1. Login successfully
2. In browser console, manually clear auth:
   ```javascript
   localStorage.removeItem('auth_credentials')
   ```
3. Make API call to trigger new request:
   - Try to click "Start Bot"
4. Verify:
   - 401 error in network tab
   - Auto-redirected to `/login`
   - localStorage cleared
   - Session lost

**Expected Result**:
- ✅ 401 error detected
- ✅ Auto-logout triggered
- ✅ Redirected to login
- ✅ Cannot access protected pages

**Failure Handling**:
- ❌ If not redirected: Check response interceptor
- ❌ If session not cleared: Check auth.logout()
- ❌ If can still access dashboard: Check auth check in layout

---

### Test 15: Network Tab Verification

**Objective**: Verify all API communications

**Steps**:
1. Open browser Dev Tools (F12)
2. Go to "Network" tab
3. Login and navigate dashboard
4. Watch network requests

**Expected Requests**:
```
1. POST /login → 401 (attempt), then depends on credentials
2. GET /api/status → 200
3. GET /api/accounts → 200
4. GET /api/analytics → 200
5. POST /api/bot/start → 200
6. POST /api/bot/stop → 200
7. GET /health → 200
```

**Verify Headers**:
Each request should have:
```
Authorization: Basic YWRtaW46Y2hhbmdlbWU=  (base64 for admin:changeme)
Content-Type: application/json
```

**Verify Responses**:
Each should return proper JSON with status field

**Expected Result**:
- ✅ All requests successful (200 status)
- ✅ Auth header present on protected endpoints
- ✅ Request/response times < 500ms
- ✅ No CORS errors
- ✅ Proper content-type headers

---

## Performance Testing

### Test 16: Page Load Performance

**Objective**: Verify page load times

**Tools**: Browser DevTools > Performance tab

**Steps**:
1. Clear cache (Network tab gear icon)
2. Go to `/dashboard`
3. Record performance
4. Check metrics:
   - First Contentful Paint (FCP): < 2s
   - Largest Contentful Paint (LCP): < 3s
   - Cumulative Layout Shift (CLS): < 0.1
   - Time to Interactive (TTI): < 4s

**Expected Result**:
- ✅ FCP < 2 seconds
- ✅ LCP < 3 seconds
- ✅ CLS stable (no layout shift)
- ✅ TTI < 4 seconds

---

### Test 17: Network Performance

**Objective**: Verify API response times

**Steps**:
1. Monitor Network tab during normal usage
2. Check response times for:
   - `/api/status` - should be < 200ms
   - `/api/accounts` - should be < 300ms
   - `/api/analytics` - should be < 300ms
   - `/api/bot/start` - should be < 500ms
   - `/api/bot/stop` - should be < 500ms

**Expected Result**:
- ✅ Status: < 200ms
- ✅ Accounts: < 300ms
- ✅ Analytics: < 300ms
- ✅ Bot actions: < 500ms

---

## Browser Compatibility

### Test 18: Cross-Browser Testing

Test in each browser:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

**Steps**: Run Test 1 (Build) through Test 14 (Error Handling) in each browser

**Expected**: All tests pass in all browsers

---

## Mobile Testing

### Test 19: Mobile Responsiveness

**Objective**: Verify dashboard works on mobile

**Steps**:
1. Open DevTools (F12)
2. Click device toggle (mobile icon)
3. Select iPhone 12 or similar
4. Navigate to `/dashboard`
5. Verify:
   - Page is responsive
   - Sidebar collapses or becomes hamburger menu
   - Charts resize properly
   - Buttons are clickable (touch-friendly)
   - Forms are usable on mobile

**Expected Result**:
- ✅ Responsive layout active
- ✅ Touch targets > 44x44px
- ✅ No horizontal scrolling
- ✅ Readable on small screens

---

## Success Criteria Summary

| Test | Type | Status | Notes |
|------|------|--------|-------|
| Build Compilation | Automated | Must Pass | 0 errors |
| Dev Server | Automated | Must Pass | Starts cleanly |
| Login Page | Manual | Must Pass | Auth works |
| Dashboard | Manual | Must Pass | All data loads |
| Bot Control | Manual | Must Pass | Start/Stop work |
| Accounts | Manual | Must Pass | CRUD operations |
| Analytics | Manual | Must Pass | Charts display |
| Navigation | Manual | Must Pass | All links work |
| Auth Persistence | Manual | Must Pass | Survives refresh |
| Konami Code | Manual | Nice-to-Have | Easter egg |
| Logo Clicks | Manual | Nice-to-Have | Easter egg |
| Quick Stats | Manual | Nice-to-Have | Easter egg |
| Error Handling | Manual | Should Pass | Graceful failures |
| Auto-Logout | Manual | Should Pass | Session management |
| Network | Manual | Should Pass | Proper API calls |
| Performance | Manual | Nice-to-Have | < 3s load time |
| Compatibility | Manual | Should Pass | Modern browsers |
| Mobile | Manual | Should Pass | Responsive |

---

## Debugging Tips

### Check Build Output
```bash
cd frontend
npm run build 2>&1 | grep -i error
```

### Check Dev Server Logs
```bash
cd frontend
npm run dev 2>&1 | head -100
```

### Check Console Errors
Open DevTools > Console and look for:
- Red error messages
- Network failures
- Missing modules

### Check Network Tab
```
Requests → filter by "Fetch/XHR"
Click on each request:
  • Headers → check Authorization
  • Response → check for errors
  • Status → should be 200 or 201
```

### Check Storage
```
DevTools → Application → Storage:
  • localStorage → check auth_credentials
  • localStorage → check easter_eggs_unlocked
  • localStorage → check achievements_unlocked
```

### Test Backend Directly
```bash
# Get status
curl -u admin:changeme http://localhost:8000/api/status

# Get accounts
curl -u admin:changeme http://localhost:8000/api/accounts

# Get analytics
curl -u admin:changeme http://localhost:8000/api/analytics
```

---

## Rollback Procedures

If tests fail and you need to rollback:

```bash
# Restore original state
git checkout frontend/lib/api.ts
git checkout frontend/lib/easter-eggs.ts

# Verify files are gone
ls frontend/lib/ | grep -E "(api|easter)"
```

---

## Sign-Off

When all tests pass:

```bash
# Verify build one final time
cd frontend && npm run build

# Check exit code
echo $?  # Should be 0
```

**Test Date**: ____________
**Tester**: ____________
**Result**: ✅ All Tests Passed / ❌ Some Tests Failed

**Notes**: ________________________

---

See `DASHBOARD_FIX_SUMMARY.md` for complete documentation.
