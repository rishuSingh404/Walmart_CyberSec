from flask import Flask, request, jsonify, Response, g
import requests
import os
import logging
from flask_cors import CORS
from functools import wraps
import json
import datetime
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("flask_adapter")

app = Flask(__name__)
CORS(app)

# Configuration
BACKEND_BASE_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')
MODEL_API_URL = os.environ.get('MODEL_API_URL', 'http://localhost:5000')

# Middleware to forward authentication headers
def forward_auth_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header
        g.headers_to_forward = headers
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Walmart Secure Flask Adapter',
        'backend_url': BACKEND_BASE_URL,
        'model_api_url': MODEL_API_URL
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    try:
        # Try to forward to backend
        try:
            response = requests.post(f"{BACKEND_BASE_URL}/api/login", json=data)
            return Response(response.content, status=response.status_code,
                          content_type=response.headers.get('Content-Type'))
        except requests.exceptions.ConnectionError:
            # If backend is not available, provide mock response
            logger.warning("Backend connection failed, providing mock response")
            email = data.get("email", "user@example.com") if data else "user@example.com"
            return jsonify({
                "access_token": "mock_jwt_token.with.signature",
                "token_type": "bearer",
                "user_id": "mock_user_123",
                "email": email,
                "role": "user"
            })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        response = requests.post(f"{BACKEND_BASE_URL}/api/signup", json=data)
        return Response(response.content, status=response.status_code,
                      content_type=response.headers.get('Content-Type'))
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-admin', methods=['GET'])
@forward_auth_header
def check_admin():
    headers = g.headers_to_forward
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/check-admin", headers=headers)
        return Response(response.content, status=response.status_code,
                      content_type=response.headers.get('Content-Type'))
    except Exception as e:
        logger.error(f"Check admin error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# === Behavioral Biometrics Endpoints ===

@app.route('/api/fingerprint/update', methods=['POST'])
@forward_auth_header
def update_fingerprint():
    headers = g.headers_to_forward
    data = request.json
    try:
        # Try to forward to backend
        try:
            response = requests.post(f"{BACKEND_BASE_URL}/api/fingerprint/update", json=data, headers=headers)
            if response.status_code != 404:
                return Response(response.content, status=response.status_code,
                              content_type=response.headers.get('Content-Type'))
        except Exception as e:
            logger.warning(f"Backend connection for fingerprint update failed: {str(e)}")
        
        # If we get here, either the endpoint returned 404 or there was an error
        # Return a mock response
        logger.info("Providing mock fingerprint update response")
        return jsonify({
            "status": "success",
            "message": "Fingerprint updated",
            "confidence_score": round(random.uniform(0.75, 0.95), 2)
        })
    except Exception as e:
        logger.error(f"Update fingerprint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/fingerprint/analyze', methods=['POST'])
@forward_auth_header
def analyze_behavior():
    headers = g.headers_to_forward
    data = request.json
    try:
        # Try to forward to backend
        try:
            response = requests.post(f"{BACKEND_BASE_URL}/api/fingerprint/analyze", json=data, headers=headers)
            if response.status_code != 404:
                return Response(response.content, status=response.status_code,
                              content_type=response.headers.get('Content-Type'))
        except Exception as e:
            logger.warning(f"Backend connection for behavior analysis failed: {str(e)}")
        
        # If we get here, either the endpoint returned 404 or there was an error
        # Return a mock response
        is_anomaly = random.random() < 0.1  # 10% chance of anomaly
        return jsonify({
            "is_anomaly": is_anomaly,
            "anomaly_score": round(random.uniform(0.05, 0.4 if not is_anomaly else 0.8), 2),
            "confidence": round(random.uniform(0.75, 0.95), 2),
            "anomalous_fields": ["typing_speed", "mouse_distance"] if is_anomaly else []
        })
    except Exception as e:
        logger.error(f"Analyze behavior error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# === Risk Assessment Endpoints ===

@app.route('/api/risk/assess', methods=['POST'])
@forward_auth_header
def assess_risk():
    headers = g.headers_to_forward
    data = request.json
    
    # First get risk score from ML model
    try:
        # Try to forward to ML model
        try:
            ml_data = {
                "typing_speed": data.get("typing_speed", 0) if data else 0,
                "mouse_distance": data.get("mouse_distance", 0) if data else 0,
                "click_count": data.get("click_count", 0) if data else 0,
                "session_duration": data.get("session_duration", 0) if data else 0,
                "scroll_depth": data.get("scroll_depth", 0) if data else 0,
                "ip_location_score": data.get("ip_location_score", 1.0) if data else 1.0,
                "device_type_score": data.get("device_type_score", 1.0) if data else 1.0,
                "timestamp": data.get("timestamp", "12:00") if data else "12:00"
            }
            
            ml_response = requests.post(f"{MODEL_API_URL}/risk-score", json=ml_data)
            
            if ml_response.status_code == 200:
                ml_result = ml_response.json()
                
                # Then forward to backend with the ML result
                if data is None:
                    data = {}
                data["ml_risk_score"] = ml_result.get("score", 0) * 100  # Convert to 0-100 scale
                data["ml_risk_label"] = ml_result.get("risk_label", "low")
                
                # Try to forward to backend
                try:
                    response = requests.post(f"{BACKEND_BASE_URL}/api/risk/assess", json=data, headers=headers)
                    if response.status_code != 404:
                        return Response(response.content, status=response.status_code,
                                      content_type=response.headers.get('Content-Type'))
                except Exception as e:
                    logger.warning(f"Backend connection for risk assess failed: {str(e)}")
        except Exception as e:
            logger.warning(f"ML model connection failed: {str(e)}")
        
        # If we get here, provide a mock response
        logger.info("Providing mock risk assessment response")
        risk_score = round(random.uniform(10, 80), 2)
        risk_label = "low"
        if risk_score > 70:
            risk_label = "high"
        elif risk_score > 40:
            risk_label = "medium"
            
        ml_score = round(risk_score * 0.6, 2)
        fingerprint_diff = round(risk_score * 0.25, 2)
        intent_score = round(risk_score * 0.15, 2)
            
        return jsonify({
            "risk_score": risk_score,
            "risk_label": risk_label,
            "component_scores": {
                "ml_score": ml_score,
                "fingerprint_diff": fingerprint_diff,
                "intent_score": intent_score
            }
        })
    except Exception as e:
        logger.error(f"Risk assessment error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# === Real-time Analytics Endpoints ===

@app.route('/api/analytics/session', methods=['GET'])
@forward_auth_header
def get_session_analytics():
    headers = g.headers_to_forward
    try:
        # Try to forward to backend
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/api/analytics/session", headers=headers)
            if response.status_code != 404:
                return Response(response.content, status=response.status_code,
                              content_type=response.headers.get('Content-Type'))
        except Exception as e:
            logger.warning(f"Backend connection for session analytics failed: {str(e)}")
        
        # If we get here, provide a mock response
        logger.info("Providing mock session analytics response")
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=random.randint(5, 60))).isoformat()
        
        return jsonify({
            "session_id": f"mock_session_{random.randint(1000, 9999)}",
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
                    "type": "page_view",
                    "timestamp": (now - datetime.timedelta(minutes=random.randint(1, 10))).isoformat(),
                    "details": {"page": "/dashboard"}
                }
            ]
        })
    except Exception as e:
        logger.error(f"Session analytics error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
@forward_auth_header
def get_dashboard_data():
    headers = g.headers_to_forward
    try:
        # Try to forward to backend
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/api/analytics/dashboard", headers=headers)
            if response.status_code != 404:
                return Response(response.content, status=response.status_code,
                              content_type=response.headers.get('Content-Type'))
        except Exception as e:
            logger.warning(f"Backend connection for dashboard data failed: {str(e)}")
        
        # If we get here, provide a mock response
        logger.info("Providing mock dashboard data response")
        return jsonify({
            "active_sessions": random.randint(5, 25),
            "high_risk_count": random.randint(0, 5),
            "login_attempts": random.randint(20, 100),
            "blocked_attempts": random.randint(0, 10)
        })
    except Exception as e:
        logger.error(f"Dashboard data error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# === Admin Endpoints ===

@app.route('/api/admin/users', methods=['GET'])
@forward_auth_header
def get_users():
    headers = g.headers_to_forward
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/admin/users", headers=headers)
        return Response(response.content, status=response.status_code,
                      content_type=response.headers.get('Content-Type'))
    except Exception as e:
        logger.error(f"Get users error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/audit-logs', methods=['GET'])
@forward_auth_header
def get_audit_logs():
    headers = g.headers_to_forward
    params = {k: v for k, v in request.args.items()}
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/admin/audit-logs", 
                              headers=headers, params=params)
        return Response(response.content, status=response.status_code,
                      content_type=response.headers.get('Content-Type'))
    except Exception as e:
        logger.error(f"Audit logs error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 