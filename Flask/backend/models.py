try:
    from .database import db
except ImportError:
    from database import db
import datetime
import json
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.mutable import MutableDict

# Removed duplicate SQLAlchemy initialization

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # Removing updated_at as it's not in the database schema
    
    # Relationships
    fingerprints = db.relationship('BehavioralData', backref='user', lazy=True, cascade="all, delete-orphan")
    risk_assessments = db.relationship('RiskAssessment', backref='user', lazy=True, cascade="all, delete-orphan")
    analytics = db.relationship('UserAnalytics', backref='user', lazy=True, cascade="all, delete-orphan")
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True, cascade="all, delete-orphan")

class BehavioralData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fingerprint_data = db.Column(MutableDict.as_mutable(JSON), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<BehavioralData {self.id} for User {self.user_id}>'

class RiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    risk_label = db.Column(db.String(20), nullable=False)  # 'low', 'medium', 'high'
    component_scores = db.Column(MutableDict.as_mutable(JSON), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<RiskAssessment {self.id} for User {self.user_id}: {self.risk_label}>'

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(MutableDict.as_mutable(JSON), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<AuditLog {self.id}: {self.action}>'

# New model for storing detailed user analytics
class UserAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(50), nullable=False)
    page_url = db.Column(db.String(255), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    # Typing metrics
    typing_wpm = db.Column(db.Float, nullable=True)
    typing_keystrokes = db.Column(db.Integer, nullable=True)
    typing_corrections = db.Column(db.Integer, nullable=True)
    
    # Mouse metrics
    mouse_clicks = db.Column(db.Integer, nullable=True)
    mouse_movements = db.Column(db.Integer, nullable=True)
    mouse_velocity = db.Column(db.Float, nullable=True)
    mouse_idle_time = db.Column(db.Integer, nullable=True)
    
    # Scroll metrics
    scroll_depth = db.Column(db.Float, nullable=True)
    scroll_speed = db.Column(db.Float, nullable=True)
    scroll_events = db.Column(db.Integer, nullable=True)
    
    # Focus metrics
    focus_changes = db.Column(db.Integer, nullable=True)
    focus_time = db.Column(db.Integer, nullable=True)
    tab_switches = db.Column(db.Integer, nullable=True)
    
    # Session metrics
    session_duration = db.Column(db.Integer, nullable=True)
    page_views = db.Column(db.Integer, nullable=True)
    interactions_count = db.Column(db.Integer, nullable=True)
    
    # Additional data - renamed from 'metadata' to 'analytics_metadata'
    analytics_metadata = db.Column(MutableDict.as_mutable(JSON), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # Removing updated_at as it's not in the database schema
    
    def __repr__(self):
        return f'<UserAnalytics {self.id} for User {self.user_id}, Session {self.session_id}>' 