#!/usr/bin/env python3
"""
Simple script to create an admin user in the database.
Usage: python create_admin_simple.py --email admin@example.com --password adminpass
"""

import argparse
import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

# Create a minimal Flask app for database operations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def create_admin_user(email, password):
    """Create an admin user in the database."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
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