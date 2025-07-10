#!/usr/bin/env python3
"""
Entry point script to run the Flask application
This script can be run directly from the backend directory
"""
import sys
import os

# Add the current directory to Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app creation function
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Walmart Secure Backend...")
    print("Server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=8000, debug=True) 