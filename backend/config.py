import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BACKEND_BASE_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')
    MODEL_API_URL = os.environ.get('MODEL_API_URL', 'http://localhost:5000') 