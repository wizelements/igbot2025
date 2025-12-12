#!/bin/bash

# IGBot 2025 - Complete Deployment Script
# Deploys both backend and frontend to Vercel

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   IGBot 2025 - Full Stack Deployment  ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI not found${NC}"
    echo "Installing Vercel CLI..."
    npm install -g vercel
    echo -e "${GREEN}✅ Vercel CLI installed${NC}"
fi

# Verify we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo -e "${RED}❌ vercel.json not found. Are you in the project root?${NC}"
    exit 1
fi

# Ask deployment type
echo -e "${YELLOW}Select deployment type:${NC}"
echo "1) Production (main deployment)"
echo "2) Preview (testing deployment)"
read -p "Enter choice (1-2): " DEPLOY_TYPE

if [ "$DEPLOY_TYPE" == "1" ]; then
    DEPLOY_CMD="vercel --prod"
    ENV_TYPE="production"
    echo -e "${GREEN}📦 Deploying to PRODUCTION${NC}"
else
    DEPLOY_CMD="vercel"
    ENV_TYPE="preview"
    echo -e "${YELLOW}📦 Deploying to PREVIEW${NC}"
fi

echo ""
echo "=========================================="
echo "Step 1: Backend API Deployment"
echo "=========================================="
echo ""

# Deploy backend
echo -e "${BLUE}Deploying backend...${NC}"
BACKEND_URL=$($DEPLOY_CMD --yes 2>&1 | grep -o 'https://[^ ]*' | head -1)

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}❌ Backend deployment failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend deployed!${NC}"
echo -e "${GREEN}   URL: $BACKEND_URL${NC}"
echo ""

# Check if environment variables are set
echo -e "${YELLOW}Checking environment variables...${NC}"

read -p "Have you set the required environment variables? (y/n): " ENV_SET

if [ "$ENV_SET" != "y" ]; then
    echo ""
    echo -e "${YELLOW}Setting up environment variables...${NC}"
    echo ""
    
    echo "Enter IG_ACCOUNTS (format: username:password:2fa_secret):"
    vercel env add IG_ACCOUNTS $ENV_TYPE
    
    echo ""
    echo "Enter DASHBOARD_USERNAME:"
    vercel env add DASHBOARD_USERNAME $ENV_TYPE
    
    echo ""
    echo "Enter DASHBOARD_PASSWORD:"
    vercel env add DASHBOARD_PASSWORD $ENV_TYPE
    
    echo ""
    echo -e "${GREEN}✅ Environment variables set${NC}"
    echo -e "${YELLOW}Redeploying backend with new environment variables...${NC}"
    
    BACKEND_URL=$($DEPLOY_CMD --yes 2>&1 | grep -o 'https://[^ ]*' | head -1)
    echo -e "${GREEN}✅ Backend redeployed: $BACKEND_URL${NC}"
fi

# Test backend
echo ""
echo -e "${BLUE}Testing backend...${NC}"
sleep 3

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")
if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Backend health check passed${NC}"
else
    echo -e "${RED}⚠️  Backend health check returned: $HTTP_CODE${NC}"
    echo "   Continuing anyway..."
fi

echo ""
echo "=========================================="
echo "Step 2: Frontend Dashboard Deployment"
echo "=========================================="
echo ""

# Navigate to frontend
cd frontend

# Set frontend environment variable
echo -e "${BLUE}Setting frontend API URL...${NC}"
echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" > .env.production
echo -e "${GREEN}✅ API URL configured${NC}"

# Add backend URL to Vercel env
echo -e "${YELLOW}Setting Vercel environment variable...${NC}"
if [ "$ENV_TYPE" == "production" ]; then
    echo "$BACKEND_URL" | vercel env add NEXT_PUBLIC_API_URL production 2>&1 | grep -q "already exists" && echo "Updating existing variable..."
else
    echo "$BACKEND_URL" | vercel env add NEXT_PUBLIC_API_URL preview 2>&1 | grep -q "already exists" && echo "Updating existing variable..."
fi

# Deploy frontend
echo ""
echo -e "${BLUE}Deploying frontend as separate project...${NC}"
echo -e "${YELLOW}Note: Frontend is a separate Vercel project${NC}"
FRONTEND_URL=$($DEPLOY_CMD --yes 2>&1 | grep -o 'https://[^ ]*' | head -1)

if [ -z "$FRONTEND_URL" ]; then
    echo -e "${RED}❌ Frontend deployment failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Frontend deployed!${NC}"
echo -e "${GREEN}   URL: $FRONTEND_URL${NC}"

# Test frontend
echo ""
echo -e "${BLUE}Testing frontend...${NC}"
sleep 3

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")
if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Frontend health check passed${NC}"
else
    echo -e "${RED}⚠️  Frontend health check returned: $HTTP_CODE${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║      Deployment Complete! 🎉           ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "Your IGBot 2025 is now live!"
echo ""
echo -e "${YELLOW}IMPORTANT: Backend and Frontend are separate Vercel projects${NC}"
echo ""
echo -e "${BLUE}Backend API:${NC}"
echo "  $BACKEND_URL"
echo "  Docs: $BACKEND_URL/docs"
echo ""
echo -e "${BLUE}Frontend Dashboard:${NC}"
echo "  $FRONTEND_URL"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Visit the frontend dashboard"
echo "  2. Login with your credentials"
echo "  3. Start the bot from the dashboard"
echo "  4. Monitor analytics"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  View logs:    vercel logs --follow"
echo "  List deploys: vercel ls"
echo "  Rollback:     vercel rollback"
echo ""
echo "=========================================="
echo "Need help? Check BUILD_DEPLOY_COMMANDS.md"
echo "=========================================="
