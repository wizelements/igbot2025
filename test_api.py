"""
Test script for API endpoints
Run this locally before deploying
"""
import requests
from requests.auth import HTTPBasicAuth

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "changeme"

auth = HTTPBasicAuth(USERNAME, PASSWORD)

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed\n")

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Root endpoint passed\n")

def test_status():
    """Test status endpoint"""
    print("🔍 Testing status endpoint...")
    response = requests.get(f"{BASE_URL}/api/status", auth=auth)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Status endpoint passed\n")

def test_accounts():
    """Test accounts endpoint"""
    print("🔍 Testing accounts endpoint...")
    response = requests.get(f"{BASE_URL}/api/accounts", auth=auth)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Accounts endpoint passed\n")

def test_config():
    """Test config endpoint"""
    print("🔍 Testing config endpoint...")
    response = requests.get(f"{BASE_URL}/api/config", auth=auth)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Config endpoint passed\n")

def test_analytics():
    """Test analytics endpoint"""
    print("🔍 Testing analytics endpoint...")
    response = requests.get(f"{BASE_URL}/api/analytics", auth=auth)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Analytics endpoint passed\n")

def test_unauthorized():
    """Test unauthorized access"""
    print("🔍 Testing unauthorized access...")
    response = requests.get(f"{BASE_URL}/api/status")
    print(f"Status: {response.status_code}")
    assert response.status_code == 401
    print("✅ Unauthorized access blocked correctly\n")

def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 IGBot 2025 API Tests")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_root()
        test_status()
        test_accounts()
        test_config()
        test_analytics()
        test_unauthorized()
        
        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        print()
        print("🚀 Ready to deploy to Vercel!")
        print("Run: vercel --prod")
        
    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ Test failed: {e}")
        print("=" * 50)
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
