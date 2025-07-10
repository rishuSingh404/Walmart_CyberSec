#!/usr/bin/env python3
"""
Test script to verify CORS and endpoint functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_cors_preflight():
    """Test CORS preflight requests"""
    print("Testing CORS preflight requests...")
    
    # Test OPTIONS request to otp_attempts
    response = requests.options(f"{BASE_URL}/otp_attempts", 
                               headers={'Origin': 'http://localhost:8080'})
    print(f"OTP attempts OPTIONS: {response.status_code}")
    print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")
    
    # Test OPTIONS request to user_analytics
    response = requests.options(f"{BASE_URL}/user_analytics", 
                               headers={'Origin': 'http://localhost:8080'})
    print(f"User analytics OPTIONS: {response.status_code}")
    print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")

def test_otp_endpoints():
    """Test OTP endpoints"""
    print("\nTesting OTP endpoints...")
    
    # Test GET request
    response = requests.get(f"{BASE_URL}/otp_attempts")
    print(f"OTP attempts GET: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
    
    # Test POST request
    test_data = {
        "otp_code": "123456",
        "user_id": 1
    }
    response = requests.post(f"{BASE_URL}/otp_attempts", 
                            json=test_data,
                            headers={'Content-Type': 'application/json'})
    print(f"OTP attempts POST: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")

def test_user_analytics_endpoints():
    """Test user analytics endpoints"""
    print("\nTesting user analytics endpoints...")
    
    # Test GET request
    response = requests.get(f"{BASE_URL}/user_analytics")
    print(f"User analytics GET: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
    
    # Test POST request
    test_data = {
        "user_id": 1,
        "event_type": "page_view",
        "page": "/dashboard"
    }
    response = requests.post(f"{BASE_URL}/user_analytics", 
                            json=test_data,
                            headers={'Content-Type': 'application/json'})
    print(f"User analytics POST: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")

def test_health_check():
    """Test health check endpoint"""
    print("\nTesting health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")

if __name__ == "__main__":
    print("Starting CORS and endpoint tests...")
    print("=" * 50)
    
    try:
        test_health_check()
        test_cors_preflight()
        test_otp_endpoints()
        test_user_analytics_endpoints()
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running on localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}") 