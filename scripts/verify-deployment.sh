#!/bin/bash

# Deployment Verification Script
# Tests all endpoints and functionality

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   Deployment Verification Tool         ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Ask for URLs
read -p "Enter backend URL (e.g., https://your-api.vercel.app): " BACKEND_URL
read -p "Enter frontend URL (e.g., https://your-app.vercel.app): " FRONTEND_URL
read -p "Enter dashboard username: " USERNAME
read -sp "Enter dashboard password: " PASSWORD
echo ""
echo ""

# Test counter
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local NAME=$1
    local URL=$2
    local EXPECTED=$3
    local AUTH=$4
    
    echo -n "Testing $NAME... "
    
    if [ -z "$AUTH" ]; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
    else
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "$USERNAME:$PASSWORD" "$URL")
    fi
    
    if [ "$HTTP_CODE" == "$EXPECTED" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $HTTP_CODE)"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC} (Expected $EXPECTED, got $HTTP_CODE)"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "Backend API Tests"
echo "=========================================="
echo ""

test_endpoint "Health Check" "$BACKEND_URL/health" "200"
test_endpoint "API Root" "$BACKEND_URL/" "200"
test_endpoint "API Docs" "$BACKEND_URL/docs" "200"
test_endpoint "Status (Auth)" "$BACKEND_URL/api/status" "200" "auth"
test_endpoint "Accounts (Auth)" "$BACKEND_URL/api/accounts" "200" "auth"
test_endpoint "Analytics (Auth)" "$BACKEND_URL/api/analytics" "200" "auth"

echo ""
echo "=========================================="
echo "Frontend Tests"
echo "=========================================="
echo ""

test_endpoint "Home Page" "$FRONTEND_URL" "200"
test_endpoint "Login Page" "$FRONTEND_URL/login" "200"
test_endpoint "Dashboard" "$FRONTEND_URL/dashboard" "200"

echo ""
echo "=========================================="
echo "Results Summary"
echo "=========================================="
echo ""

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo -e "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "Success Rate: ${PERCENTAGE}%"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════╗"
    echo "║   All Tests Passed! 🎉                 ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Your deployment is working correctly!"
    echo ""
    echo "Next steps:"
    echo "  1. Visit: $FRONTEND_URL"
    echo "  2. Login with your credentials"
    echo "  3. Start using the bot!"
    exit 0
else
    echo -e "${RED}"
    echo "╔════════════════════════════════════════╗"
    echo "║   Some Tests Failed ⚠️                  ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check environment variables"
    echo "  2. View logs: vercel logs --follow"
    echo "  3. Verify credentials"
    echo "  4. Check deployment status: vercel ls"
    exit 1
fi
