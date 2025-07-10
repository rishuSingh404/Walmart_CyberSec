# Walmart Cybersecurity Demo

This project demonstrates advanced cybersecurity features including:

- User behavior analytics
- Biometric authentication
- Risk assessment
- Real-time monitoring

## Project Structure

- **Backend**: Flask-based API with ML integration
- **Frontend**: React application with TypeScript and Tailwind CSS
- **Model**: Machine learning models for risk assessment

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Quick Start

1. Clone the repository
2. Run the all-in-one script:

```bash
./run_all.bat
```

This will:
- Create a Python virtual environment
- Install backend dependencies
- Start the backend server
- Install frontend dependencies
- Start the frontend development server

### Manual Setup

#### Backend

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the server
python -m backend.app
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

## Features

### Authentication

- User registration and login
- JWT-based authentication
- Role-based access control

### Biometric Analysis

- Typing pattern analysis
- Mouse movement tracking
- Behavioral fingerprinting

### Risk Assessment

- ML-based risk scoring
- Real-time risk alerts
- Multi-factor authentication triggers

### Real-time Monitoring

- WebSocket-based real-time updates
- Admin dashboard for monitoring
- User session tracking

## API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `GET /api/check-admin` - Admin verification

### Risk Assessment
- `POST /api/risk/assess` - Main risk assessment
- `POST /risk-score` - Compatibility endpoint

### Analytics
- `GET /user_analytics` - Get analytics overview
- `POST /user_analytics` - Submit analytics data
- `POST /api/analytics/store` - Store user analytics
- `GET /api/analytics/user/<user_id>` - Get user analytics

### OTP & Security
- `GET /otp_attempts` - Get OTP statistics
- `POST /otp_attempts` - Submit OTP attempt

### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/audit-logs` - Get audit logs
- `GET /api/analytics/dashboard` - Get dashboard data

## WebSocket Events

### Client to Server
- `authenticate` - Authenticate with token
- `join_admin_room` - Join admin monitoring room
- `risk_alert` - Send risk alert
- `user_activity` - Track user activity

### Server to Client
- `auth_response` - Authentication result
- `user_status` - User online/offline status
- `high_risk_alert` - High risk notifications
- `user_activity_update` - User activity updates

## License

This project is for demonstration purposes only. 