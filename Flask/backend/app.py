from flask import Flask, request, jsonify, g
from flask_cors import CORS
import logging
import random
import datetime

# Use absolute imports instead of relative imports
from config import Config
from database import db, init_app as init_db
from models import User, BehavioralData, RiskAssessment, AuditLog, UserAnalytics
from auth import (
    hash_password,
    verify_password,
    create_token,
    token_required,
    admin_required,
)
from biometrics import analyze_user_behavior
from risk_assessment import assess_user_risk
from websocket import init_socketio

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
    
    # Initialize SocketIO
    socketio = init_socketio(app)

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
                        'id': str(i),
                        'user_id': str(random.randint(1, 10)),
                        'session_id': f'session_{random.randint(1000, 9999)}',
                        'risk_score': round(random.uniform(10, 90), 1),
                        'otp_code': f'{random.randint(100000, 999999)}',
                        'is_valid': random.choice([True, False]),
                        'ip_address': f'192.168.1.{random.randint(1, 255)}',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'created_at': (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))).isoformat(),
                        'metadata': {
                            'product_views': [random.randint(1, 50) for _ in range(random.randint(1, 5))],
                            'cart_actions': random.randint(0, 10),
                            'wishlist_actions': random.randint(0, 5),
                            'category_changes': random.randint(0, 8),
                            'searches': random.randint(0, 15)
                        }
                    } for i in range(1, 11)
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
            try:
                total_users = User.query.count()
                active_users = random.randint(total_users // 2, total_users)
            except Exception as e:
                # Fallback if database is not available
                total_users = 0
                active_users = 0
            
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
                
            try:
                # Log analytics event
                log_entry = AuditLog(
                    user_id=data.get('user_id'),
                    action='analytics_event',
                    details=data
                )
                db.session.add(log_entry)
                db.session.commit()
            except Exception as e:
                # Fallback if database is not available
                return jsonify({
                    'success': True,
                    'message': 'Analytics data recorded (mock)',
                    'event_id': random.randint(1000, 9999)
                })
            
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

    # === User Analytics Storage Endpoints ===
    @app.route('/api/analytics/store', methods=['POST'])
    @token_required
    def store_user_analytics(current_user):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Create a new UserAnalytics record
        analytics = UserAnalytics(
            user_id=current_user.id,
            session_id=data.get('sessionId', ''),
            page_url=data.get('pageUrl'),
            user_agent=data.get('userAgent'),
            
            # Typing metrics
            typing_wpm=data.get('typing', {}).get('wpm'),
            typing_keystrokes=data.get('typing', {}).get('keystrokes'),
            typing_corrections=data.get('typing', {}).get('backspaces'),
            
            # Mouse metrics
            mouse_clicks=data.get('mouse', {}).get('clicks'),
            mouse_movements=data.get('mouse', {}).get('totalDistance'),
            mouse_velocity=data.get('mouse', {}).get('averageSpeed'),
            mouse_idle_time=data.get('mouse', {}).get('idleTime'),
            
            # Scroll metrics
            scroll_depth=data.get('scroll', {}).get('maxDepth'),
            scroll_speed=data.get('scroll', {}).get('scrollSpeed'),
            scroll_events=data.get('scroll', {}).get('totalScrollDistance'),
            
            # Focus metrics
            focus_changes=data.get('focus', {}).get('focusEvents') + data.get('focus', {}).get('blurEvents', 0),
            focus_time=data.get('focus', {}).get('totalFocusTime'),
            tab_switches=data.get('focus', {}).get('tabSwitches'),
            
            # Session metrics
            session_duration=data.get('sessionDuration'),
            interactions_count=data.get('typing', {}).get('keystrokes', 0) + data.get('mouse', {}).get('clicks', 0),
            
            # Store the original data as analytics_metadata
            analytics_metadata=data
        )
        
        db.session.add(analytics)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Analytics data stored",
            "analytics_id": analytics.id
        })

    @app.route('/api/analytics/user/<int:user_id>', methods=['GET'])
    @token_required
    def get_user_analytics(current_user, user_id):
        # Only allow users to access their own data or admins
        if current_user.id != user_id and current_user.role != 'admin':
            return jsonify({"error": "Unauthorized"}), 403

        # Get user's analytics
        analytics = UserAnalytics.query.filter_by(user_id=user_id).order_by(UserAnalytics.created_at.desc()).limit(50).all()

        return jsonify([{
            'id': record.id,
            'session_id': record.session_id,
            'page_url': record.page_url,
            'typing_wpm': record.typing_wpm,
            'mouse_clicks': record.mouse_clicks,
            'scroll_depth': record.scroll_depth,
            'focus_time': record.focus_time,
            'session_duration': record.session_duration,
            'created_at': record.created_at.isoformat(),
            'analytics_metadata': record.analytics_metadata
        } for record in analytics])

    # === Risk Score Endpoint (for compatibility) ===
    @app.route('/risk-score', methods=['POST'])
    def risk_score_endpoint():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # For non-authenticated users, create a simplified assessment
        # This is useful for the shop page where users might not be logged in
        user_id = data.get('user_id')
        user = None
        
        if user_id:
            user = User.query.get(user_id)
        
        if not user:
            # Create a simplified risk assessment for non-authenticated users
            risk_score = random.uniform(20, 80)
            risk_label = "high" if risk_score > 70 else "medium" if risk_score > 40 else "low"
            
            return jsonify({
                "risk_score": risk_score,
                "risk_label": risk_label,
                "component_scores": {
                    "ml_score": random.uniform(20, 80),
                    "ml_risk_label": risk_label,
                    "fingerprint_diff": random.uniform(0, 50),
                    "intent_score": random.uniform(10, 30)
                }
            })
        
        # If user is authenticated, use the proper risk assessment
        assessment_result = assess_user_risk(user, data)
        return jsonify(assessment_result)

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
    socketio = init_socketio(app)
    
    if socketio:
        # Run with SocketIO for real-time features
        socketio.run(app, host='0.0.0.0', port=8000, debug=True)
    else:
        # Fallback to regular Flask app
        app.run(host='0.0.0.0', port=8000, debug=True) 