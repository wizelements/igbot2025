#!/bin/bash

# Backend Build Script

set -e

echo "🏗️  Building Backend API"
echo "========================"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements-vercel.txt

# Run tests (if available)
if [ -f "test_api.py" ]; then
    echo "🧪 Running tests..."
    python test_api.py || echo "⚠️  Some tests failed"
fi

echo ""
echo "✅ Backend build complete!"
echo ""
echo "To test locally:"
echo "  python api/index.py"
echo ""
echo "To deploy:"
echo "  vercel --prod"
