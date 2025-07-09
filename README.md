# Walmart Secure Backend

A comprehensive Flask-based backend system for Walmart's secure authentication, behavioral biometrics, risk assessment, and real-time analytics platform.

## 🏗️ Architecture Overview

This backend implements a multi-layered security system with:

- **Authentication Layer**: JWT-based user and admin authentication
- **Behavioral Biometrics**: User behavior analysis and fingerprinting
- **Risk Assessment**: ML-powered risk scoring with multiple components
- **Real-time Analytics**: Session tracking and dashboard metrics
- **Admin Management**: User management and system monitoring

## 📁 Project Structure

```
flask/
├── backend/                    # Main backend application
│   ├── __init__.py
│   ├── app.py                 # Main Flask application with all routes
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database setup and initialization
│   ├── models.py              # SQLAlchemy models (User, BehavioralData, etc.)
│   ├── auth.py                # Authentication utilities (JWT, password hashing)
│   ├── biometrics.py          # Behavioral biometrics analysis
│   ├── risk_assessment.py     # Risk assessment logic
│   ├── ml_integration.py      # Machine learning model integration
│   ├── create_admin.py        # Admin user creation script
│   └── requirements.txt       # Python dependencies
├── model/                     # Trained ML models
│   ├── risk_model.joblib      # Risk assessment model
│   ├── risk_scaler.joblib     # Feature scaler
│   ├── risk_label_encoder.joblib  # Label encoder
│   └── train_model.py         # Model training script
├── rebuild_and_run.bat        # Complete setup and run script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows (for batch scripts) or Linux/Mac (manual setup)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd flask
   ```

2. **Run the complete setup script**
   ```bash
   # Windows
   .\rebuild_and_run.bat
   
   # Linux/Mac (manual setup)
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
   python backend/create_admin.py --email admin@walmart.com --password AdminPassword123
   python -m flask --app backend.app run --host=0.0.0.0 --port=8000
   ```

3. **Verify the backend is running**
   ```bash
   curl http://localhost:8000/
   # Should return: {"service":"Walmart Secure Backend","status":"healthy"}
   ```

## 🔐 Authentication System

### User Registration
```http
POST /api/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

### User Login
```http
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com",
  "role": "user"
}
```

### Admin Authentication
- **Default Admin**: `admin@walmart.com` / `AdminPassword123`
- Use the same `/api/login` endpoint
- Admin users have access to additional endpoints

## 🎯 API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/signup` | POST | Register new user | No |
| `/api/login` | POST | User/Admin login | No |
| `/api/check-admin` | GET | Verify admin status | Admin |

### Behavioral Biometrics Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/fingerprint/update` | POST | Update user behavioral data | User |
| `/api/fingerprint/analyze` | POST | Analyze behavioral patterns | User |

**Fingerprint Update Example:**
```http
POST /api/fingerprint/update
Authorization: Bearer <token>
Content-Type: application/json

{
  "typing_speed": 100,
  "mouse_distance": 500,
  "click_count": 10,
  "session_duration": 120
}
```

### Risk Assessment Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/risk/assess` | POST | Assess user risk level | User |

**Risk Assessment Example:**
```http
POST /api/risk/assess
Authorization: Bearer <token>
Content-Type: application/json

{
  "typing_speed": 100,
  "mouse_distance": 500,
  "click_count": 10,
  "session_duration": 120,
  "scroll_depth": 80,
  "ip_location_score": 0.9,
  "device_type_score": 1.0
}
```

**Response:**
```json
{
  "risk_label": "medium",
  "risk_score": 40.59,
  "component_scores": {
    "fingerprint_diff": 13.0,
    "intent_score": 13.05,
    "ml_risk_label": "low",
    "ml_score": 58.97
  }
}
```

### Analytics Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/analytics/session` | GET | Get session analytics | User |
| `/api/analytics/dashboard` | GET | Get dashboard metrics | Admin |

### Admin Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/admin/users` | GET | List all users | Admin |
| `/api/admin/audit-logs` | GET | Get audit logs | Admin |

## 🤖 Machine Learning Integration

The system includes a trained machine learning model for risk assessment:

- **Model Type**: Ensemble (Random Forest + Decision Tree)
- **Features**: Typing speed, mouse behavior, session data, device info
- **Output**: Risk labels (low/medium/high) with confidence scores
- **Location**: `model/risk_model.joblib`

### Model Features
- `typing_speed`: Characters per minute
- `mouse_distance`: Total mouse movement distance
- `click_count`: Number of clicks in session
- `session_duration`: Session length in seconds
- `scroll_depth`: Page scroll percentage
- `ip_location_score`: Geographic risk score (0-1)
- `device_type_score`: Device trust score (0-1)
- `hour`: Hour of day (derived from timestamp)

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(80) NOT NULL DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Behavioral Data Table
```sql
CREATE TABLE behavioral_data (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    fingerprint_data JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

### Risk Assessment Table
```sql
CREATE TABLE risk_assessment (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    risk_score FLOAT NOT NULL,
    risk_label VARCHAR(50) NOT NULL,
    component_scores JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

### Audit Logs Table
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(200) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details JSON,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

## 🔧 Configuration

The system uses environment-based configuration:

```python
# backend/config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///walmart_secure.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
```

## 🔒 Security Features

### JWT Authentication
- **Token Expiration**: 24 hours
- **Algorithm**: HS256
- **Payload**: User ID, email, role, expiration

### Password Security
- **Hashing**: bcrypt with salt
- **Verification**: Secure password comparison

### CORS Configuration
- **Enabled**: Yes
- **Origin**: All origins (`*`)
- **Methods**: GET, POST, OPTIONS
- **Headers**: Authorization, Content-Type

## 📊 Risk Assessment Components

The risk assessment combines multiple factors:

1. **Behavioral Fingerprint Analysis** (40%)
   - Typing patterns
   - Mouse movement patterns
   - Click behavior

2. **Intent Analysis** (30%)
   - Session duration
   - Page interactions
   - Navigation patterns

3. **Machine Learning Model** (30%)
   - Trained on historical data
   - Feature-based risk scoring
   - Ensemble prediction

## 🚨 Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `201`: Created (user registration)
- `400`: Bad Request (invalid data)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `409`: Conflict (user already exists)
- `500`: Internal Server Error

## 🔄 Frontend Integration

### Example Frontend Usage

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'user@example.com',
        password: 'password123'
    })
});

const { access_token } = await loginResponse.json();

// Risk Assessment
const riskResponse = await fetch('http://localhost:8000/api/risk/assess', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: JSON.stringify({
        typing_speed: 100,
        mouse_distance: 500,
        click_count: 10,
        session_duration: 120,
        scroll_depth: 80,
        ip_location_score: 0.9,
        device_type_score: 1.0
    })
});

const riskData = await riskResponse.json();
console.log('Risk Level:', riskData.risk_label);
console.log('Risk Score:', riskData.risk_score);
```

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python -m flask --app backend.app run --host=0.0.0.0 --port=8000 --debug
```

### Database Management
```bash
# Create admin user
python backend/create_admin.py --email admin@example.com --password adminpass

# Reset database (delete walmart_secure.db file)
rm walmart_secure.db
```

### Testing Endpoints
```bash
# Health check
curl http://localhost:8000/

# User signup
curl -X POST http://localhost:8000/api/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# User login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 📈 Performance Considerations

- **Database**: SQLite for development, PostgreSQL for production
- **Caching**: Consider Redis for session data
- **Load Balancing**: Use Gunicorn for production deployment
- **Monitoring**: Implement logging and metrics collection

## 🔮 Future Enhancements

- [ ] Real-time WebSocket connections
- [ ] Advanced behavioral analytics
- [ ] Multi-factor authentication
- [ ] API rate limiting
- [ ] Comprehensive audit trails
- [ ] Automated threat detection
- [ ] Mobile app support

## 📞 Support

For questions or issues:
1. Check the API documentation above
2. Review the error logs
3. Test with the provided examples
4. Contact the backend development team

---

**Walmart Secure Backend** - Built with Flask, SQLAlchemy, and Machine Learning for secure user authentication and risk assessment. 