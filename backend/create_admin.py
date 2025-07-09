import argparse
import sys
import os

# This is a workaround to make the script runnable from the root directory
# where the 'backend' package is.
sys.path.insert(0, os.getcwd())

from backend.app import create_app
from backend.database import db
from backend.models import User
from backend.auth import hash_password

def create_admin(email, password):
    """Creates an admin user."""
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email=email).first():
            print(f"User with email {email} already exists.")
            return

        hashed_pwd = hash_password(password)
        admin_user = User(email=email, password_hash=hashed_pwd, role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {email} created successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new admin user.')
    parser.add_argument('--email', type=str, required=True, help='Email for the admin user.')
    parser.add_argument('--password', type=str, required=True, help='Password for the admin user.')
    args = parser.parse_args()
    
    create_admin(args.email, args.password) 