#!/bin/bash

# 🚀 Frontend Deployment Script for Vercel
# This script helps you deploy the Next.js frontend to Vercel

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Main script
clear
print_header "IGBot 2025 - Frontend Deployment to Vercel"

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    print_error "frontend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_warning "Vercel CLI not found. Installing..."
    npm install -g vercel
    print_success "Vercel CLI installed!"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

print_success "Prerequisites check passed!"

# Navigate to frontend directory
cd frontend

print_header "Step 1: Installing Dependencies"
if [ ! -d "node_modules" ]; then
    print_info "Installing npm packages..."
    npm install
    print_success "Dependencies installed!"
else
    print_info "Dependencies already installed"
fi

print_header "Step 2: Testing Local Build"
print_info "Building frontend locally to check for errors..."

if npm run build; then
    print_success "Local build successful!"
else
    print_error "Local build failed!"
    echo "Please fix the errors above before deploying."
    exit 1
fi

print_header "Step 3: Deployment Options"
echo "Choose your deployment method:"
echo ""
echo "  1) Deploy with Vercel CLI (Recommended)"
echo "  2) Get Manual Instructions (for Vercel Dashboard)"
echo "  3) Exit"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        print_header "Deploying with Vercel CLI"
        
        # Check if user is logged in
        if ! vercel whoami &> /dev/null; then
            print_info "Please login to Vercel..."
            vercel login
        fi
        
        print_success "Logged in to Vercel!"
        
        # Ask for backend URL
        echo ""
        print_info "What is your backend API URL?"
        echo "Example: https://igbot2025-1.vercel.app"
        read -p "Backend URL: " backend_url
        
        if [ -z "$backend_url" ]; then
            print_error "Backend URL is required!"
            exit 1
        fi
        
        # Create .env.local for deployment
        echo "NEXT_PUBLIC_API_URL=$backend_url" > .env.local
        print_success "Environment variable configured!"
        
        # Deploy to Vercel
        print_info "Deploying to Vercel..."
        echo ""
        
        if vercel --prod; then
            print_success "Deployment successful!"
            echo ""
            print_header "🎉 Success!"
            echo "Your frontend is now deployed!"
            echo ""
            print_info "Next steps:"
            echo "  1. Visit your deployment URL (shown above)"
            echo "  2. Login with your credentials"
            echo "  3. Try the Konami Code: ↑↑↓↓←→←→BA"
            echo "  4. Complete achievements to learn best practices"
            echo ""
        else
            print_error "Deployment failed!"
            echo "Check the error messages above for details."
            exit 1
        fi
        ;;
        
    2)
        print_header "Manual Deployment Instructions"
        echo ""
        echo "Follow these steps in Vercel Dashboard:"
        echo ""
        echo "1. Go to: https://vercel.com/new"
        echo ""
        echo "2. Import your repository and click 'Configure Project'"
        echo ""
        echo "3. CRITICAL - Set Root Directory:"
        echo "   Click 'Edit' next to 'Root Directory'"
        echo "   Enter: frontend"
        echo ""
        echo "4. Add Environment Variable:"
        echo "   Name: NEXT_PUBLIC_API_URL"
        echo "   Value: [Your backend URL from first deployment]"
        echo "   Example: https://igbot2025-1.vercel.app"
        echo ""
        echo "5. Click 'Deploy' and wait ~2 minutes"
        echo ""
        echo "6. Test your deployment:"
        echo "   - Visit the URL Vercel provides"
        echo "   - Login with your credentials"
        echo "   - Try the easter eggs!"
        echo ""
        ;;
        
    3)
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice!"
        exit 1
        ;;
esac

print_header "Additional Resources"
echo "📚 Documentation:"
echo "  - FRONTEND_DEPLOYMENT_FIX.md - Complete troubleshooting guide"
echo "  - README_WEB_INTERFACE.md - Feature overview with easter eggs"
echo "  - QUICK_START_WEB.md - Quick setup guide"
echo ""
echo "🎮 Easter Eggs Worth \$3,747/year:"
echo "  - Konami Code (↑↑↓↓←→←→BA) - Premium analytics"
echo "  - Type 'godmode' - Advanced controls"
echo "  - Click logo 10x - Time traveler mode"
echo "  - Press Ctrl+Shift+M - Matrix mode"
echo "  - Press B - Batch operations"
echo "  - Press ? - Quick stats widget"
echo ""
echo "🏆 Complete all 8 achievements to unlock learning guides!"
echo ""

print_success "Deployment process complete!"
