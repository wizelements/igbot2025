#!/bin/bash

# IGBot 2025 - Vercel Deployment Script
# This script automates the deployment process

set -e

echo "🚀 IGBot 2025 - Vercel Deployment Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI not found${NC}"
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo -e "${RED}❌ vercel.json not found. Are you in the project root?${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Pre-flight checks passed${NC}"
echo ""

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Deploy to production"
echo "2) Deploy to preview"
echo "3) Set up environment variables"
echo "4) View logs"
echo "5) Check deployment status"
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}📦 Deploying to production...${NC}"
        vercel --prod
        echo ""
        echo -e "${GREEN}✅ Deployment complete!${NC}"
        echo ""
        echo "Your bot is now live! 🎉"
        echo "Visit: https://your-project.vercel.app"
        ;;
    2)
        echo ""
        echo -e "${YELLOW}📦 Deploying preview...${NC}"
        vercel
        echo ""
        echo -e "${GREEN}✅ Preview deployment complete!${NC}"
        ;;
    3)
        echo ""
        echo "Setting up environment variables..."
        echo ""
        echo "Required variables:"
        echo "- IG_ACCOUNTS"
        echo "- DASHBOARD_USERNAME"
        echo "- DASHBOARD_PASSWORD"
        echo ""
        read -p "Do you want to add environment variables now? (y/n): " add_env
        
        if [ "$add_env" = "y" ]; then
            echo ""
            echo "Add IG_ACCOUNTS (format: username:password:2fa_secret)"
            vercel env add IG_ACCOUNTS
            
            echo ""
            echo "Add DASHBOARD_USERNAME"
            vercel env add DASHBOARD_USERNAME
            
            echo ""
            echo "Add DASHBOARD_PASSWORD"
            vercel env add DASHBOARD_PASSWORD
            
            echo ""
            echo -e "${GREEN}✅ Environment variables added!${NC}"
            echo "Don't forget to redeploy: vercel --prod"
        fi
        ;;
    4)
        echo ""
        echo -e "${YELLOW}📋 Fetching logs...${NC}"
        vercel logs --follow
        ;;
    5)
        echo ""
        echo -e "${YELLOW}📊 Checking deployment status...${NC}"
        vercel ls
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Need help? Check DEPLOYMENT.md"
echo "=========================================="
