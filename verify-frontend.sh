#!/bin/bash

# IGBot 2025 - Frontend Verification Script
# Checks if everything is set up correctly

set -e

echo "🔍 IGBot 2025 - Frontend Verification"
echo "======================================"
echo ""

SUCCESS_COUNT=0
TOTAL_CHECKS=10

# Check 1: Node.js
echo "1. Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo "   ✅ Node.js $NODE_VERSION installed"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ Node.js not found"
fi

# Check 2: NPM
echo "2. Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo "   ✅ npm $NPM_VERSION installed"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ npm not found"
fi

# Check 3: Frontend directory
echo "3. Checking frontend directory..."
if [ -d "frontend" ]; then
    echo "   ✅ Frontend directory exists"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ Frontend directory not found"
fi

# Check 4: package.json
echo "4. Checking package.json..."
if [ -f "frontend/package.json" ]; then
    echo "   ✅ package.json found"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ package.json not found"
fi

# Check 5: node_modules
echo "5. Checking dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo "   ✅ Dependencies installed"
    ((SUCCESS_COUNT++))
else
    echo "   ⚠️  Dependencies not installed (run: cd frontend && npm install)"
fi

# Check 6: Environment file
echo "6. Checking environment configuration..."
if [ -f "frontend/.env.local" ]; then
    echo "   ✅ .env.local found"
    ((SUCCESS_COUNT++))
else
    echo "   ⚠️  .env.local not found (run: cd frontend && cp .env.example .env.local)"
fi

# Check 7: TypeScript config
echo "7. Checking TypeScript configuration..."
if [ -f "frontend/tsconfig.json" ]; then
    echo "   ✅ tsconfig.json found"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ tsconfig.json not found"
fi

# Check 8: Tailwind config
echo "8. Checking Tailwind CSS configuration..."
if [ -f "frontend/tailwind.config.ts" ]; then
    echo "   ✅ tailwind.config.ts found"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ tailwind.config.ts not found"
fi

# Check 9: Next.js config
echo "9. Checking Next.js configuration..."
if [ -f "frontend/next.config.js" ]; then
    echo "   ✅ next.config.js found"
    ((SUCCESS_COUNT++))
else
    echo "   ❌ next.config.js not found"
fi

# Check 10: Key files
echo "10. Checking key application files..."
REQUIRED_FILES=(
    "frontend/app/page.tsx"
    "frontend/app/login/page.tsx"
    "frontend/app/dashboard/page.tsx"
    "frontend/lib/api.ts"
    "frontend/lib/easter-eggs.ts"
    "frontend/components/Sidebar.tsx"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        ALL_FILES_EXIST=false
        echo "   ❌ Missing: $file"
    fi
done

if [ "$ALL_FILES_EXIST" = true ]; then
    echo "   ✅ All key files present"
    ((SUCCESS_COUNT++))
fi

echo ""
echo "======================================"
echo "Results: $SUCCESS_COUNT/$TOTAL_CHECKS checks passed"
echo "======================================"
echo ""

if [ $SUCCESS_COUNT -eq $TOTAL_CHECKS ]; then
    echo "🎉 Perfect! Everything is set up correctly!"
    echo ""
    echo "Next steps:"
    echo "1. cd frontend"
    echo "2. npm run dev"
    echo "3. Open http://localhost:3000"
    echo "4. Login with: admin / changeme"
    echo "5. Try the easter eggs! 🎮"
    echo ""
elif [ $SUCCESS_COUNT -ge 7 ]; then
    echo "✅ Good! Most things are set up."
    echo "Fix the warnings above, then you're ready!"
    echo ""
    echo "Quick fix:"
    echo "cd frontend && npm install"
    echo "cp .env.example .env.local"
    echo ""
elif [ $SUCCESS_COUNT -ge 5 ]; then
    echo "⚠️  Some issues found. Please run:"
    echo "./setup-frontend.sh"
    echo ""
else
    echo "❌ Multiple issues found."
    echo "Please run the setup script:"
    echo "./setup-frontend.sh"
    echo ""
fi

# Port check
echo "Checking if ports are available..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 3000 is already in use"
    echo "   Stop the process or use a different port"
else
    echo "✅ Port 3000 is available"
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Port 8000 is in use (backend running?)"
else
    echo "⚠️  Port 8000 is not in use (start backend with: python api/index.py)"
fi

echo ""
echo "🚀 Ready to automate Instagram!"
