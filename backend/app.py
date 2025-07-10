from flask import Flask, request, jsonify, g
from flask_cors import CORS
import logging
import random
import datetime

try:
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
except ImportError:
    # Fallback for direct execution
    from config import Config
    from database import db, init_app as init_db
    from models import User, BehavioralData, RiskAssessment, AuditLog
    from auth import (
        hash_password,
        verify_password,
        create_token,
        token_required,
        admin_required,
    )
    from biometrics import analyze_user_behavior
    from risk_assessment import assess_user_risk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("walmart_secure_backend")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enhanced CORS configuration
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080", "http://127.0.0.1:3000"]),
         methods=app.config.get('CORS_METHODS', ["GET", "POST", "PUT", "DELETE", "OPTIONS"]),
         allow_headers=app.config.get('CORS_ALLOW_HEADERS', ["Content-Type", "Authorization", "X-Requested-With"]),
         supports_credentials=app.config.get('CORS_SUPPORTS_CREDENTIALS', True))
    
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

    # === OTP Endpoints ===
    @app.route('/otp_attempts', methods=['GET', 'POST', 'OPTIONS'])
    def otp_attempts():
        if request.method == 'OPTIONS':
            return jsonify({'message': 'OK'}), 200
            
        if request.method == 'GET':
            # Return OTP attempt statistics
            return jsonify({
                'total_attempts': random.randint(50, 200),
                'successful_attempts': random.randint(40, 180),
                'failed_attempts': random.randint(5, 20),
                'blocked_attempts': random.randint(0, 10),
                'recent_attempts': [
                    {
                        'id': i,
                        'user_id': random.randint(1, 10),
                        'email': f'user{i}@example.com',
                        'status': random.choice(['success', 'failed', 'blocked']),
                        'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))).isoformat(),
                        'ip_address': f'192.168.1.{random.randint(1, 255)}'
                    } for i in range(1, 6)
                ]
            })
        
        elif request.method == 'POST':
            # Handle new OTP attempt
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            # Mock OTP validation
            otp_code = data.get('otp_code', '')
            user_id = data.get('user_id')
            
            # Simulate OTP validation
            is_valid = len(otp_code) == 6 and otp_code.isdigit()
            
            # Log the attempt
            log_entry = AuditLog(
                user_id=user_id,
                action='otp_attempt',
                details={
                    'otp_code': otp_code[:2] + '****',  # Mask for security
                    'success': is_valid,
                    'ip_address': request.remote_addr
                }
            )
            db.session.add(log_entry)
            db.session.commit()
            
            return jsonify({
                'success': is_valid,
                'message': 'OTP validated successfully' if is_valid else 'Invalid OTP code',
                'attempt_id': log_entry.id
            })
        
        # Default response for unsupported methods
        return jsonify({'error': 'Method not allowed'}), 405

    # === User Analytics Endpoints ===
    @app.route('/user_analytics', methods=['GET', 'POST', 'OPTIONS'])
    def user_analytics():
        if request.method == 'OPTIONS':
            return jsonify({'message': 'OK'}), 200
            
        if request.method == 'GET':
            # Return user analytics data
            total_users = User.query.count()
            active_users = random.randint(total_users // 2, total_users)
            
            return jsonify({
                'total_users': total_users,
                'active_users': active_users,
                'new_users_today': random.randint(0, 10),
                'login_success_rate': round(random.uniform(85, 98), 2),
                'average_session_duration': random.randint(300, 1800),
                'risk_distribution': {
                    'low': random.randint(60, 80),
                    'medium': random.randint(15, 30),
                    'high': random.randint(1, 10)
                },
                'top_activities': [
                    {'activity': 'login', 'count': random.randint(100, 500)},
                    {'activity': 'risk_assessment', 'count': random.randint(50, 200)},
                    {'activity': 'profile_update', 'count': random.randint(20, 100)}
                ],
                'hourly_activity': [
                    {'hour': i, 'activity_count': random.randint(10, 100)} 
                    for i in range(24)
                ]
            })
        
        elif request.method == 'POST':
            # Handle analytics data submission
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            # Log analytics event
            log_entry = AuditLog(
                user_id=data.get('user_id'),
                action='analytics_event',
                details=data
            )
            db.session.add(log_entry)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Analytics data recorded',
                'event_id': log_entry.id
            })
        
        # Default response for unsupported methods
        return jsonify({'error': 'Method not allowed'}), 405

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

    # === Error Handlers ===
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found', 'message': 'The requested endpoint does not exist'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed', 'message': 'The HTTP method is not supported for this endpoint'}), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True) 