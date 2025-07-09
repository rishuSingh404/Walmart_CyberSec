#!/usr/bin/env python3
"""
Token extraction script for verification testing.
Extracts JWT token from login response JSON.
"""

import sys
import json

def extract_token():
    """Extract token from stdin JSON response."""
    try:
        # Read JSON from stdin
        response_text = sys.stdin.read().strip()
        
        # Parse JSON response
        response_data = json.loads(response_text)
        
        # Extract token from response
        if 'access_token' in response_data:
            return response_data['access_token']
        elif 'token' in response_data:
            return response_data['token']
        else:
            return "NO_TOKEN_FOUND"
            
    except (json.JSONDecodeError, KeyError, Exception) as e:
        return "NO_TOKEN_FOUND"

if __name__ == "__main__":
    token = extract_token()
    print(token) 