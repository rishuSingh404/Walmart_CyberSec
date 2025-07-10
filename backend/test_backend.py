#!/usr/bin/env python3
"""
Test script for the backend endpoints
Can be run from the backend directory
"""
import sys
import os
import requests
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the Flask app is running.")
        return False

def test_cors_preflight():
    """Test CORS preflight requests"""
    print("\nTesting CORS preflight...")
    
    try:
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
        
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        return False

def test_otp_endpoints():
    """Test OTP endpoints"""
    print("\nTesting OTP endpoints...")
    
    try:
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
        
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        return False

def test_user_analytics_endpoints():
    """Test user analytics endpoints"""
    print("\nTesting user analytics endpoints...")
    
    try:
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
        
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        return False

def main():
    print("=" * 50)
    print("Walmart Secure Backend Test")
    print("=" * 50)
    
    # Test if server is running
    if not test_health_check():
        print("\nServer is not running. Please start the server first:")
        print("python run_app.py")
        return
    
    # Run all tests
    test_cors_preflight()
    test_otp_endpoints()
    test_user_analytics_endpoints()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("If all tests passed, your CORS issues should be resolved.")

if __name__ == "__main__":
    main() 