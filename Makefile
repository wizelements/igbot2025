# IGBot 2025 - Makefile
# Quick commands for building and deploying

.PHONY: help install dev build deploy test clean

# Default target
help:
	@echo "IGBot 2025 - Available Commands"
	@echo "================================"
	@echo ""
	@echo "Development:"
	@echo "  make install         Install all dependencies"
	@echo "  make dev             Run development servers"
	@echo "  make dev-backend     Run backend only"
	@echo "  make dev-frontend    Run frontend only"
	@echo ""
	@echo "Build:"
	@echo "  make build           Build both frontend and backend"
	@echo "  make build-frontend  Build frontend only"
	@echo "  make build-backend   Build backend only"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy          Deploy to production"
	@echo "  make deploy-backend  Deploy backend only"
	@echo "  make deploy-frontend Deploy frontend only"
	@echo "  make deploy-preview  Deploy preview"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make test-api        Test API endpoints"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean           Clean build artifacts"
	@echo "  make logs            View deployment logs"
	@echo "  make status          Check deployment status"
	@echo ""

# Installation
install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-vercel.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Development
dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@make -j2 dev-backend dev-frontend

dev-backend:
	@echo "Starting backend server..."
	python api/index.py

dev-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

# Build
build: build-backend build-frontend

build-backend:
	@echo "Building backend..."
	pip install -r requirements-vercel.txt
	@echo "Backend ready!"

build-frontend:
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "Frontend built!"

# Deployment
deploy:
	@echo "Deploying full stack to production..."
	@echo ""
	@echo "Step 1: Deploying backend..."
	vercel --prod
	@echo ""
	@echo "Step 2: Deploying frontend..."
	cd frontend && vercel --prod
	@echo ""
	@echo "Deployment complete!"

deploy-backend:
	@echo "Deploying backend to production..."
	vercel --prod

deploy-frontend:
	@echo "Deploying frontend to production..."
	cd frontend && vercel --prod

deploy-preview:
	@echo "Deploying preview..."
	vercel
	cd frontend && vercel

# Testing
test: test-api

test-api:
	@echo "Testing API endpoints..."
	python test_api.py

test-frontend:
	@echo "Testing frontend..."
	cd frontend && npm run lint

# Utilities
clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/.next
	rm -rf frontend/out
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

logs:
	@echo "Fetching deployment logs..."
	vercel logs --follow

logs-backend:
	@echo "Fetching backend logs..."
	vercel logs --follow

logs-frontend:
	@echo "Fetching frontend logs..."
	cd frontend && vercel logs --follow

status:
	@echo "Checking deployment status..."
	vercel ls

# Environment setup
env-setup:
	@echo "Setting up environment variables..."
	@echo ""
	@echo "Backend environment variables:"
	vercel env add IG_ACCOUNTS
	vercel env add DASHBOARD_USERNAME
	vercel env add DASHBOARD_PASSWORD
	@echo ""
	@echo "Frontend environment variables:"
	cd frontend && vercel env add NEXT_PUBLIC_API_URL
	@echo ""
	@echo "Environment setup complete!"

# Git helpers
push:
	git add .
	git commit -m "Update"
	git push

# Health checks
health:
	@echo "Checking health..."
	curl -f http://localhost:8000/health || echo "Local backend not running"

# Full setup for new deployment
setup: install env-setup deploy
	@echo ""
	@echo "=========================================="
	@echo "Setup complete!"
	@echo "=========================================="
	@echo ""
	@echo "Next steps:"
	@echo "1. Test your backend: make health"
	@echo "2. View logs: make logs"
	@echo "3. Check status: make status"
	@echo ""
