# Flask Adapter for Walmart Secure

This adapter provides a Flask-based API that bridges between frontend applications and the Walmart Secure backend services.

## Features Provided

The adapter exposes endpoints that map to the existing Walmart Secure backend services:

### 1. Behavioral Biometrics
- Mouse movement tracking
- Typing pattern analysis
- Scroll behavior monitoring
- Focus and attention tracking

### 2. Risk Assessment Engine
- Dynamic risk scoring
- Anomaly detection
- Fraud prevention
- Adaptive authentication

### 3. Real-time Analytics
- Live dashboard monitoring
- Instant threat alerts
- Session activity tracking
- Automated responses

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Access to the Walmart Secure backend API
- Access to the Risk Model API

### Installation

1. **Set up the environment:**
   ```
   # Windows
   start_flask.bat
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - `BACKEND_URL`: URL of the Walmart Secure backend API (default: http://localhost:8000)
   - `MODEL_API_URL`: URL of the risk model API (default: http://localhost:5000)

3. **Run the adapter:**
   ```
   # Windows
   start_flask.bat
   
   # Linux/Mac
   export BACKEND_URL=http://localhost:8000
   export MODEL_API_URL=http://localhost:5000
   python app.py
   ```

## Running the Application (Windows, PowerShell)

To start both the Flask backend and the React frontend together, use the provided PowerShell script:

1. Open PowerShell in the project root directory (`Walmart_CyberSec`).
2. Run the following command:
   
   ```powershell
   powershell -ExecutionPolicy Bypass -File start_app.ps1
   ```

This will automatically launch both the Flask API (on port 5001) and the React frontend (usually on port 3000).

- Make sure you have installed all Python dependencies (`pip install -r flask/requirements.txt`) and Node.js dependencies (`npm install`) before running the script.
- For real data, ensure the backend service is running on port 8000 and the risk model API is running on port 5000.

If you encounter issues, see the Troubleshooting section below.

## How to Run the Full Stack Application

### Quick Start (Recommended)

1. **Open PowerShell in the project root directory** (where `start_app.ps1` is located).
2. **Run the following command:**
   
   ```powershell
   powershell -ExecutionPolicy Bypass -File start_app.ps1
   ```
   This will automatically:
   - Install Python and Node.js dependencies (if not already installed)
   - Start the Flask backend (http://localhost:5001)
   - Start the React frontend (http://localhost:3000)

3. **Access the app:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Flask API: [http://localhost:5001](http://localhost:5001)

> **Note:**
> - Ensure you have Python 3.8+ and Node.js installed.
> - The backend API (http://localhost:8000) and risk model API (http://localhost:5000) must also be running for full functionality (see Troubleshooting section).

### Manual Start (Advanced)

1. **Start Flask backend:**
   ```powershell
   cd flask
   start_flask.bat
   ```
2. **Start React frontend:**
   ```powershell
   cd ..
   npm install
   npm start
   ```

## API Documentation

### Authentication

All authentication endpoints work the same way as the original backend:

- **POST /api/login**
  - **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "password123",
      "behavior_metrics": {
        "typing_speed": 250.5,
        "mouse_distance": 1200.75,
        "click_count": 5,
        "typing_interval_variance": 0.2,
        "session_duration": 15000.0,
        "scroll_depth": 0.75
      }
    }
    ```
  - **Response:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

- **POST /api/signup**
  - **Request Body:** Same as login
  - **Response:** Same as login

- **GET /api/check-admin**
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**
    ```json
    {
      "is_admin": true
    }
    ```

### Behavioral Biometrics

- **POST /api/fingerprint/update**
  - **Headers:** `Authorization: Bearer <token>`
  - **Request Body:**
    ```json
    {
      "typing_speed": 250.5,
      "mouse_distance": 1200.75,
      "click_count": 5,
      "typing_interval_variance": 0.2,
      "session_duration": 15000.0,
      "scroll_depth": 0.75
    }
    ```
  - **Response:**
    ```json
    {
      "status": "success",
      "message": "Fingerprint updated",
      "confidence_score": 0.85
    }
    ```

- **POST /api/fingerprint/analyze**
  - **Headers:** `Authorization: Bearer <token>`
  - **Request Body:** Same as update
  - **Response:**
    ```json
    {
      "is_anomaly": false,
      "anomaly_score": 0.15,
      "confidence": 0.85,
      "anomalous_fields": []
    }
    ```

### Risk Assessment

- **POST /api/risk/assess**
  - **Headers:** `Authorization: Bearer <token>`
  - **Request Body:**
    ```json
    {
      "typing_speed": 250.5,
      "mouse_distance": 1200.75,
      "click_count": 5,
      "session_duration": 15000.0,
      "scroll_depth": 0.75,
      "ip_location_score": 0.95,
      "device_type_score": 1.0,
      "timestamp": "14:30"
    }
    ```
  - **Response:**
    ```json
    {
      "risk_score": 25.5,
      "risk_label": "low",
      "component_scores": {
        "ml_score": 15.0,
        "fingerprint_diff": 18.5,
        "intent_score": 10.0
      }
    }
    ```

### Real-time Analytics

- **GET /api/analytics/session**
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**
    ```json
    {
      "session_id": "abc123",
      "start_time": "2023-07-08T14:30:00Z",
      "duration": 1200,
      "risk_level": "low",
      "events": [...]
    }
    ```

- **GET /api/analytics/dashboard**
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**
    ```json
    {
      "active_sessions": 15,
      "high_risk_count": 2,
      "login_attempts": 45,
      "blocked_attempts": 5
    }
    ```

### Admin Endpoints

- **GET /api/admin/users**
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**
    ```json
    {
      "users": [
        {
          "id": "user1",
          "email": "user1@example.com",
          "risk_level": "low"
        },
        ...
      ]
    }
    ```

- **GET /api/admin/audit-logs**
  - **Headers:** `Authorization: Bearer <token>`
  - **Query Parameters:**
    - `start_date`: (optional) ISO date string
    - `end_date`: (optional) ISO date string
    - `user_id`: (optional) Filter by user ID
  - **Response:**
    ```json
    {
      "logs": [
        {
          "id": "log1",
          "timestamp": "2023-07-08T14:30:00Z",
          "user_id": "user1",
          "action": "login",
          "details": {...}
        },
        ...
      ]
    }
    ```

## Integration Guide for Frontend Developers

### Step 1: Configure Your Frontend

1. **Update API Base URL:**
   
   In your API configuration/service file:
   ```javascript
   // Example in React
   const API_BASE_URL = 'http://localhost:5001';
   ```

2. **Include Authentication Headers:**
   
   After login, store the JWT token and include it in subsequent requests:
   ```javascript
   // Store token after login
   localStorage.setItem('token', response.data.access_token);
   
   // Include in requests
   axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`;
   ```

### Step 2: Collect Behavioral Data

Create a utility to collect behavioral metrics:

```javascript
// behavior-collector.js
class BehaviorCollector {
  constructor() {
    this.startTime = Date.now();
    this.keyPresses = [];
    this.mouseDistance = 0;
    this.clickCount = 0;
    this.scrollDepth = 0;
    this.lastMousePosition = { x: 0, y: 0 };
    
    // Initialize listeners
    this.initializeListeners();
  }
  
  initializeListeners() {
    // Track key presses
    document.addEventListener('keydown', this.handleKeyPress.bind(this));
    
    // Track mouse movement
    document.addEventListener('mousemove', this.handleMouseMove.bind(this));
    
    // Track clicks
    document.addEventListener('click', this.handleClick.bind(this));
    
    // Track scrolling
    window.addEventListener('scroll', this.handleScroll.bind(this));
  }
  
  handleKeyPress(event) {
    this.keyPresses.push({
      key: event.key,
      timestamp: Date.now()
    });
  }
  
  handleMouseMove(event) {
    const { clientX, clientY } = event;
    if (this.lastMousePosition.x !== 0 && this.lastMousePosition.y !== 0) {
      const dx = clientX - this.lastMousePosition.x;
      const dy = clientY - this.lastMousePosition.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      this.mouseDistance += distance;
    }
    this.lastMousePosition = { x: clientX, y: clientY };
  }
  
  handleClick() {
    this.clickCount++;
  }
  
  handleScroll() {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
    const clientHeight = document.documentElement.clientHeight;
    
    this.scrollDepth = scrollTop / (scrollHeight - clientHeight) || 0;
  }
  
  getMetrics() {
    const sessionDuration = Date.now() - this.startTime;
    
    // Calculate typing speed and variance
    let typingSpeed = 0;
    let typingIntervalVariance = 0;
    
    if (this.keyPresses.length > 1) {
      const intervals = [];
      for (let i = 1; i < this.keyPresses.length; i++) {
        intervals.push(this.keyPresses[i].timestamp - this.keyPresses[i-1].timestamp);
      }
      
      // Average interval
      typingSpeed = intervals.reduce((sum, val) => sum + val, 0) / intervals.length;
      
      // Calculate variance
      const mean = typingSpeed;
      const squareDiffs = intervals.map(interval => {
        const diff = interval - mean;
        return diff * diff;
      });
      typingIntervalVariance = Math.sqrt(
        squareDiffs.reduce((sum, val) => sum + val, 0) / intervals.length
      ) / mean;
    }
    
    return {
      typing_speed: typingSpeed,
      mouse_distance: this.mouseDistance,
      click_count: this.clickCount,
      typing_interval_variance: typingIntervalVariance,
      session_duration: sessionDuration,
      scroll_depth: this.scrollDepth
    };
  }
  
  cleanup() {
    document.removeEventListener('keydown', this.handleKeyPress.bind(this));
    document.removeEventListener('mousemove', this.handleMouseMove.bind(this));
    document.removeEventListener('click', this.handleClick.bind(this));
    window.removeEventListener('scroll', this.handleScroll.bind(this));
  }
}

export default BehaviorCollector;
```

### Step 3: Use the Collected Data with the API

```javascript
// auth-service.js
import axios from 'axios';

const API_URL = 'http://localhost:5001';

// Login with behavioral metrics
export const login = async (email, password, behaviorMetrics) => {
  try {
    const response = await axios.post(`${API_URL}/api/login`, {
      email,
      password,
      behavior_metrics: behaviorMetrics
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
    }
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Assess risk
export const assessRisk = async (behaviorMetrics) => {
  try {
    const response = await axios.post(`${API_URL}/api/risk/assess`, behaviorMetrics);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update fingerprint
export const updateFingerprint = async (behaviorMetrics) => {
  try {
    const response = await axios.post(`${API_URL}/api/fingerprint/update`, behaviorMetrics);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Get session analytics
export const getSessionAnalytics = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/analytics/session`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
```

### Step 4: Integration Example in a React Component

```jsx
import React, { useEffect, useState } from 'react';
import BehaviorCollector from './behavior-collector';
import { login, assessRisk } from './auth-service';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [collector, setCollector] = useState(null);
  
  useEffect(() => {
    // Initialize behavior collector
    const newCollector = new BehaviorCollector();
    setCollector(newCollector);
    
    return () => {
      newCollector.cleanup();
    };
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!collector) return;
    
    try {
      // Get behavior metrics
      const metrics = collector.getMetrics();
      
      // Call login API with metrics
      const result = await login(email, password, metrics);
      
      // Handle successful login
      console.log('Logged in successfully!', result);
      
      // Redirect based on user role
      // ...
    } catch (error) {
      console.error('Login failed:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Email:</label>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          required 
        />
      </div>
      <div>
        <label>Password:</label>
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginForm;
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure that both backend API and risk model API are running
   - Check the configured URLs in environment variables

2. **Authentication Errors**
   - Verify that the JWT token is being properly stored and included in requests
   - Check that token format is correct: `Authorization: Bearer <token>`

3. **CORS Errors**
   - The adapter has CORS enabled for all origins by default
   - If you're still seeing CORS errors, verify your frontend is making requests correctly

### Getting Help

If you encounter any issues with integration, please check:

1. Verify that all services are running:
   - Flask adapter (http://localhost:5001)
   - Backend API (http://localhost:8000)
   - Risk model API (http://localhost:5000)

2. Check the Flask adapter logs for any errors

3. Contact the backend developer for assistance