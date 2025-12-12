#!/bin/bash

# IGBot 2025 - Frontend Setup Script
# Automates the setup process for the web interface

set -e

echo "🎨 IGBot 2025 - Frontend Setup"
echo "================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version must be 18 or higher"
    echo "Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "📦 node_modules found. Cleaning..."
    rm -rf node_modules package-lock.json
fi

echo "📦 Installing dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo ""
    echo "🔧 Creating environment configuration..."
    
    read -p "Enter your API URL (default: http://localhost:8000): " API_URL
    API_URL=${API_URL:-http://localhost:8000}
    
    echo "NEXT_PUBLIC_API_URL=$API_URL" > .env.local
    echo "✅ Environment file created"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Start the backend API (if not running)"
echo "2. Run: npm run dev"
echo "3. Open: http://localhost:3000"
echo "4. Login with: admin / changeme"
echo ""
echo "🎮 Don't forget to try the Easter eggs!"
echo ""
echo "🚀 Happy automating!"
