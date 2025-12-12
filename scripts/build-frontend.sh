#!/bin/bash

# Frontend Build Script

set -e

echo "🏗️  Building Frontend Dashboard"
echo "================================"
echo ""

cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Lint code
echo "🔍 Linting code..."
npm run lint || echo "⚠️  Lint warnings found"

# Build
echo "🔨 Building Next.js application..."
npm run build

echo ""
echo "✅ Frontend build complete!"
echo ""
echo "Output directory: .next"
echo ""
echo "To test locally:"
echo "  npm start"
echo ""
echo "To deploy:"
echo "  vercel --prod"
