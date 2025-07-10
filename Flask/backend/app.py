from flask import Flask, jsonify, request
from flask import Flask, jsonify, request, make_response
from flask_cors import cross_origin
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

    @app.before_request
    def handle_options_requests():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', request.headers.get('Access-Control-Request-Headers'))
            response.headers.add('Access-Control-Allow-Methods', request.headers.get('Access-Control-Request-Method'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response




    init_db(app)








    @app.route('/health', methods=['GET'])
    def health_check():
        response = jsonify({
            'status': 'healthy',
            'service': 'Walmart Secure Backend',
        })

        return response

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


    @app.route('/otp_attempts', methods=['GET'])


    @token_required
    def get_otp_attempts(current_user):
        attempts = AuditLog.query.filter(AuditLog.action.like('OTP_%')).order_by(AuditLog.timestamp.desc()).all()
        return jsonify([
            {
                'id': attempt.id,
                'user_id': attempt.user_id,
                'session_id': attempt.details.get('session_id'),
                'risk_score': attempt.details.get('risk_score'),
                'otp_code': attempt.action,
                'is_valid': attempt.details.get('is_valid'),
                'ip_address': attempt.details.get('ip_address'),
                'user_agent': attempt.details.get('user_agent'),
                'created_at': attempt.timestamp.isoformat(),
                'metadata': attempt.details.get('metadata')
            } for attempt in attempts
        ])

    @app.route('/user_analytics', methods=['GET'])


    @token_required
    def get_user_analytics(current_user):
        analytics_data = BehavioralData.query.order_by(BehavioralData.created_at.desc()).all()
        return jsonify([
            {
                'id': data.id,
                'user_id': data.user_id,
                'session_id': data.fingerprint_data.get('session_id'),
                'page_url': data.fingerprint_data.get('page_url'),
                'user_agent': data.fingerprint_data.get('user_agent'),
                'typing_wpm': data.fingerprint_data.get('typing_wpm'),
                'typing_keystrokes': data.fingerprint_data.get('typing_keystrokes'),
                'typing_corrections': data.fingerprint_data.get('typing_corrections'),
                'mouse_clicks': data.fingerprint_data.get('mouse_clicks'),
                'mouse_movements': data.fingerprint_data.get('mouse_movements'),
                'mouse_velocity': data.fingerprint_data.get('mouse_velocity'),
                'mouse_idle_time': data.fingerprint_data.get('mouse_idle_time'),
                'scroll_depth': data.fingerprint_data.get('scroll_depth'),
                'scroll_speed': data.fingerprint_data.get('scroll_speed'),
                'scroll_events': data.fingerprint_data.get('scroll_events'),
                'focus_changes': data.fingerprint_data.get('focus_changes'),
                'focus_time': data.fingerprint_data.get('focus_time'),
                'tab_switches': data.fingerprint_data.get('tab_switches'),
                'session_duration': data.fingerprint_data.get('session_duration'),
                'page_views': data.fingerprint_data.get('page_views'),
                'interactions_count': data.fingerprint_data.get('interactions_count'),
                'created_at': data.created_at.isoformat(),
                'updated_at': data.created_at.isoformat(), # Assuming updated_at is same as created_at for simplicity
                'metadata': data.fingerprint_data.get('metadata')
            } for data in analytics_data
        ])

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