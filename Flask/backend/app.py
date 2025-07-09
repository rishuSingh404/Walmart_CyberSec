from flask import Flask, request, jsonify, g
from flask_cors import CORS
import logging
import random
import datetime

from .config import Config
from .database import db, init_app as init_db
from .models import User, BehavioralData, RiskAssessment, AuditLog
from .auth import (
    hash_password,
    verify_password,
    create_token,
    token_required,
    admin_required,
)
from .biometrics import analyze_user_behavior
from .risk_assessment import assess_user_risk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("walmart_secure_backend")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_db(app)

    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Walmart Secure Backend',
        })

    # === Authentication Endpoints ===
    @app.route('/api/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 409

        hashed_pwd = hash_password(data['password'])
        new_user = User(email=data['email'], password_hash=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not verify_password(data['password'], user.password_hash):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        token = create_token(user.id, user.email, user.role)

        return jsonify({
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        })

    @app.route('/api/check-admin', methods=['GET'])
    @admin_required
    def check_admin(current_user):
        return jsonify({'message': 'Welcome, admin!', 'user': {'email': current_user.email, 'role': current_user.role}})


    # === Behavioral Biometrics Endpoints ===
    @app.route('/api/fingerprint/update', methods=['POST'])
    @token_required
    def update_fingerprint(current_user):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        new_fingerprint = BehavioralData(user_id=current_user.id, fingerprint_data=data)
        db.session.add(new_fingerprint)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Fingerprint updated",
            "confidence_score": round(random.uniform(0.75, 0.95), 2) # Mock score
        })

    @app.route('/api/fingerprint/analyze', methods=['POST'])
    @token_required
    def analyze_behavior(current_user):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        analysis_result = analyze_user_behavior(current_user, data)

        return jsonify(analysis_result)

    # === Risk Assessment Endpoints ===
    @app.route('/api/risk/assess', methods=['POST'])
    @token_required
    def assess_risk(current_user):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        assessment_result = assess_user_risk(current_user, data)
        return jsonify(assessment_result)

    # === Real-time Analytics Endpoints ===
    @app.route('/api/analytics/session', methods=['GET'])
    @token_required
    def get_session_analytics(current_user):
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=random.randint(5, 60))).isoformat()
        
        return jsonify({
            "session_id": f"mock_session_{random.randint(1000, 9999)}",
            "user_id": current_user.id,
            "start_time": start_time,
            "duration": random.randint(300, 3600),
            "risk_level": random.choice(["low", "medium", "high"]),
            "events": [
                {
                    "type": "login",
                    "timestamp": start_time,
                    "details": {"success": True}
                },
                {
                    "type": "risk_assessment",
                    "timestamp": (now - datetime.timedelta(minutes=random.randint(1, 10))).isoformat(),
                    "details": {"score": round(random.uniform(20, 80), 2)}
                }
            ]
        })


    @app.route('/api/analytics/dashboard', methods=['GET'])
    @admin_required
    def get_dashboard_data(current_user):
        active_sessions = User.query.count()
        high_risk_count = RiskAssessment.query.filter(RiskAssessment.risk_label == 'high').count()
        login_attempts = AuditLog.query.filter(AuditLog.action == 'login_success').count()
        
        return jsonify({
            "active_sessions": active_sessions,
            "high_risk_count": high_risk_count,
            "login_attempts": login_attempts,
            "blocked_attempts": random.randint(0, 10)
        })

    # === Admin Endpoints ===
    @app.route('/api/admin/users', methods=['GET'])
    @admin_required
    def get_users(current_user):
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        } for user in users])

    @app.route('/api/admin/audit-logs', methods=['GET'])
    @admin_required
    def get_audit_logs(current_user):
        logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
        return jsonify([{
            'id': log.id,
            'user_id': log.user_id,
            'action': log.action,
            'timestamp': log.timestamp.isoformat(),
            'details': log.details
        } for log in logs])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True) 