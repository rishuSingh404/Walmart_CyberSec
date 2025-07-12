#!/usr/bin/env python3
"""
Script to create an admin user in the database.
Usage: python create_admin.py --email admin@example.com --password adminpass
"""

import argparse
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db
from models import User
from auth import hash_password

def create_admin_user(email, password):
    """Create an admin user in the database."""
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User {email} already exists. Updating role to admin...")
            existing_user.role = 'admin'
            db.session.commit()
            print(f"User {email} role updated to admin.")
            return
        
        # Create new admin user
        hashed_password = hash_password(password)
        admin_user = User(
            email=email,
            password_hash=hashed_password,
            role='admin'
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {email} created successfully!")

def main():
    parser = argparse.ArgumentParser(description='Create an admin user')
    parser.add_argument('--email', required=True, help='Admin email')
    parser.add_argument('--password', required=True, help='Admin password')
    
    args = parser.parse_args()
    
    try:
        create_admin_user(args.email, args.password)
    except Exception as e:
        print(f"Error creating admin user: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 