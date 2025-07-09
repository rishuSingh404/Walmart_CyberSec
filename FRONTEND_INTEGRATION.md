# Frontend Integration Guide - Walmart Secure Backend

This guide provides step-by-step instructions for frontend developers to integrate with the Walmart Secure Backend API.

## 🚀 Quick Start

### 1. Backend Setup (One-time)
```bash
# Clone the backend repository
git clone <backend-repo-url>
cd flask

# Run the setup script (Windows)
.\rebuild_and_run.bat

# Or manual setup (Linux/Mac)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
python backend/create_admin.py --email admin@walmart.com --password AdminPassword123
python -m flask --app backend.app run --host=0.0.0.0 --port=8000
```

### 2. Verify Backend is Running
```bash
curl http://localhost:8000/
# Should return: {"service":"Walmart Secure Backend","status":"healthy"}
```

## 🔐 Authentication Flow

### Step 1: User Registration
```javascript
// Register a new user
const registerUser = async (email, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    if (response.ok) {
      const data = await response.json();
      console.log('User registered:', data.message);
      return true;
    } else {
      const error = await response.json();
      console.error('Registration failed:', error.message);
      return false;
    }
  } catch (error) {
    console.error('Registration error:', error);
    return false;
  }
};

// Usage
await registerUser('user@example.com', 'StrongPassword123');
```

### Step 2: User Login
```javascript
// Login and get JWT token
const loginUser = async (email, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    if (response.ok) {
      const data = await response.json();
      
      // Store token in localStorage or secure storage
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('userRole', data.role);
      localStorage.setItem('userId', data.user_id);
      
      console.log('Login successful:', data);
      return data;
    } else {
      const error = await response.json();
      console.error('Login failed:', error.message);
      return null;
    }
  } catch (error) {
    console.error('Login error:', error);
    return null;
  }
};

// Usage
const userData = await loginUser('user@example.com', 'StrongPassword123');
if (userData) {
  // Redirect to dashboard or main app
  console.log('Welcome,', userData.email);
}
```

### Step 3: Admin Login
```javascript
// Admin login (same endpoint, different credentials)
const adminData = await loginUser('admin@walmart.com', 'AdminPassword123');
if (adminData && adminData.role === 'admin') {
  console.log('Admin access granted');
  // Show admin dashboard
}
```

## 🎯 API Integration Examples

### Authentication Helper
```javascript
// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

// Helper function to check if user is logged in
const isAuthenticated = () => {
  const token = localStorage.getItem('authToken');
  return token !== null;
};

// Helper function to logout
const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('userRole');
  localStorage.removeItem('userId');
  // Redirect to login page
  window.location.href = '/login';
};
```

### Behavioral Biometrics Collection
```javascript
// Behavior tracking class
class BehaviorTracker {
  constructor() {
    this.startTime = Date.now();
    this.keyPresses = [];
    this.mouseDistance = 0;
    this.clickCount = 0;
    this.scrollDepth = 0;
    this.lastMousePosition = { x: 0, y: 0 };
    
    this.initializeTracking();
  }

  initializeTracking() {
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

  getBehaviorData() {
    const sessionDuration = (Date.now() - this.startTime) / 1000; // in seconds
    
    // Calculate typing speed (characters per minute)
    let typingSpeed = 0;
    if (this.keyPresses.length > 1) {
      const timeSpan = (this.keyPresses[this.keyPresses.length - 1].timestamp - this.keyPresses[0].timestamp) / 1000;
      typingSpeed = (this.keyPresses.length / timeSpan) * 60; // chars per minute
    }

    return {
      typing_speed: typingSpeed,
      mouse_distance: this.mouseDistance,
      click_count: this.clickCount,
      session_duration: sessionDuration,
      scroll_depth: this.scrollDepth * 100 // as percentage
    };
  }

  cleanup() {
    document.removeEventListener('keydown', this.handleKeyPress.bind(this));
    document.removeEventListener('mousemove', this.handleMouseMove.bind(this));
    document.removeEventListener('click', this.handleClick.bind(this));
    window.removeEventListener('scroll', this.handleScroll.bind(this));
  }
}
```

### Update Behavioral Fingerprint
```javascript
// Update user's behavioral fingerprint
const updateFingerprint = async (behaviorData) => {
  try {
    const response = await fetch('http://localhost:8000/api/fingerprint/update', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(behaviorData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Fingerprint updated:', data);
      return data;
    } else {
      const error = await response.json();
      console.error('Fingerprint update failed:', error);
      return null;
    }
  } catch (error) {
    console.error('Fingerprint update error:', error);
    return null;
  }
};

// Usage with behavior tracker
const tracker = new BehaviorTracker();

// After user interaction, update fingerprint
const behaviorData = tracker.getBehaviorData();
await updateFingerprint(behaviorData);
```

### Risk Assessment
```javascript
// Assess user risk level
const assessRisk = async (behaviorData) => {
  try {
    // Add additional risk factors
    const riskData = {
      ...behaviorData,
      ip_location_score: 0.9, // Mock value - replace with actual IP analysis
      device_type_score: 1.0, // Mock value - replace with actual device analysis
      timestamp: new Date().toISOString()
    };

    const response = await fetch('http://localhost:8000/api/risk/assess', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(riskData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Risk assessment:', data);
      return data;
    } else {
      const error = await response.json();
      console.error('Risk assessment failed:', error);
      return null;
    }
  } catch (error) {
    console.error('Risk assessment error:', error);
    return null;
  }
};

// Usage
const riskResult = await assessRisk(behaviorData);
if (riskResult) {
  console.log('Risk Level:', riskResult.risk_label);
  console.log('Risk Score:', riskResult.risk_score);
  
  // Handle different risk levels
  switch (riskResult.risk_label) {
    case 'low':
      // Normal user experience
      break;
    case 'medium':
      // Additional verification
      showAdditionalVerification();
      break;
    case 'high':
      // Block access or require re-authentication
      showHighRiskWarning();
      break;
  }
}
```

### Analytics Integration
```javascript
// Get session analytics
const getSessionAnalytics = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/analytics/session', {
      method: 'GET',
      headers: getAuthHeaders()
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Session analytics:', data);
      return data;
    } else {
      const error = await response.json();
      console.error('Analytics failed:', error);
      return null;
    }
  } catch (error) {
    console.error('Analytics error:', error);
    return null;
  }
};

// Get dashboard analytics (admin only)
const getDashboardAnalytics = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/analytics/dashboard', {
      method: 'GET',
      headers: getAuthHeaders()
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Dashboard analytics:', data);
      return data;
    } else {
      const error = await response.json();
      console.error('Dashboard analytics failed:', error);
      return null;
    }
  } catch (error) {
    console.error('Dashboard analytics error:', error);
    return null;
  }
};
```

## 🔧 React Integration Example

### Authentication Context
```jsx
// AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    const userRole = localStorage.getItem('userRole');
    const userId = localStorage.getItem('userId');
    
    if (token && userRole && userId) {
      setUser({
        token,
        role: userRole,
        id: userId
      });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('authToken', data.access_token);
        localStorage.setItem('userRole', data.role);
        localStorage.setItem('userId', data.user_id);
        
        setUser({
          token: data.access_token,
          role: data.role,
          id: data.user_id,
          email: data.email
        });
        
        return { success: true };
      } else {
        const error = await response.json();
        return { success: false, error: error.message };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

### Login Component
```jsx
// Login.jsx
import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(email, password);
    
    if (result.success) {
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <h2>Login to Walmart Secure</h2>
      {error && <div className="error">{error}</div>}
      
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
        
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;
```

### Dashboard with Risk Assessment
```jsx
// Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { BehaviorTracker } from './BehaviorTracker';

const Dashboard = () => {
  const { user } = useAuth();
  const [riskLevel, setRiskLevel] = useState(null);
  const [tracker, setTracker] = useState(null);

  useEffect(() => {
    // Initialize behavior tracking
    const newTracker = new BehaviorTracker();
    setTracker(newTracker);

    // Cleanup on unmount
    return () => {
      if (newTracker) {
        newTracker.cleanup();
      }
    };
  }, []);

  const performRiskAssessment = async () => {
    if (!tracker) return;

    const behaviorData = tracker.getBehaviorData();
    
    try {
      const response = await fetch('http://localhost:8000/api/risk/assess', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify({
          ...behaviorData,
          ip_location_score: 0.9,
          device_type_score: 1.0
        })
      });

      if (response.ok) {
        const data = await response.json();
        setRiskLevel(data.risk_label);
        
        // Update fingerprint
        await fetch('http://localhost:8000/api/fingerprint/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${user.token}`
          },
          body: JSON.stringify(behaviorData)
        });
      }
    } catch (error) {
      console.error('Risk assessment failed:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Welcome, {user.email}</h1>
      <p>Role: {user.role}</p>
      
      <div className="risk-section">
        <h3>Security Status</h3>
        {riskLevel && (
          <div className={`risk-level ${riskLevel}`}>
            Risk Level: {riskLevel.toUpperCase()}
          </div>
        )}
        <button onClick={performRiskAssessment}>
          Assess Risk
        </button>
      </div>
      
      {user.role === 'admin' && (
        <div className="admin-section">
          <h3>Admin Panel</h3>
          <button onClick={() => window.location.href = '/admin/users'}>
            Manage Users
          </button>
          <button onClick={() => window.location.href = '/admin/analytics'}>
            View Analytics
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
```

## 🎨 CSS Styling Examples

```css
/* Risk level indicators */
.risk-level {
  padding: 10px;
  border-radius: 5px;
  font-weight: bold;
  margin: 10px 0;
}

.risk-level.low {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.risk-level.medium {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.risk-level.high {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Login form styling */
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.login-container form div {
  margin-bottom: 15px;
}

.login-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.login-container input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-container button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}
```

## 🚨 Error Handling

### API Error Handler
```javascript
// apiErrorHandler.js
export const handleApiError = (error, response) => {
  if (response) {
    switch (response.status) {
      case 401:
        // Unauthorized - redirect to login
        localStorage.removeItem('authToken');
        window.location.href = '/login';
        return 'Session expired. Please login again.';
      
      case 403:
        // Forbidden - insufficient permissions
        return 'You do not have permission to perform this action.';
      
      case 404:
        // Not found
        return 'The requested resource was not found.';
      
      case 409:
        // Conflict
        return 'A resource with this information already exists.';
      
      case 500:
        // Server error
        return 'An internal server error occurred. Please try again later.';
      
      default:
        return 'An unexpected error occurred.';
    }
  } else if (error.name === 'TypeError') {
    return 'Network error. Please check your connection.';
  } else {
    return error.message || 'An unknown error occurred.';
  }
};
```

## 📱 Mobile Integration

### React Native Example
```javascript
// React Native API calls
const API_BASE_URL = 'http://localhost:8000';

const loginUser = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    
    if (response.ok) {
      // Store token securely (use AsyncStorage or secure storage)
      await AsyncStorage.setItem('authToken', data.access_token);
      return { success: true, data };
    } else {
      return { success: false, error: data.message };
    }
  } catch (error) {
    return { success: false, error: 'Network error' };
  }
};

// Mobile behavior tracking
import { Dimensions } from 'react-native';

class MobileBehaviorTracker {
  constructor() {
    this.startTime = Date.now();
    this.touchCount = 0;
    this.scrollDistance = 0;
    this.screenSize = Dimensions.get('window');
  }

  handleTouch = () => {
    this.touchCount++;
  };

  handleScroll = (event) => {
    this.scrollDistance += Math.abs(event.nativeEvent.contentOffset.y);
  };

  getBehaviorData() {
    const sessionDuration = (Date.now() - this.startTime) / 1000;
    
    return {
      touch_count: this.touchCount,
      scroll_distance: this.scrollDistance,
      session_duration: sessionDuration,
      device_width: this.screenSize.width,
      device_height: this.screenSize.height
    };
  }
}
```

## 🔒 Security Best Practices

1. **Token Storage**: Use secure storage for JWT tokens
2. **HTTPS**: Always use HTTPS in production
3. **Token Expiration**: Handle token expiration gracefully
4. **Input Validation**: Validate all user inputs
5. **Error Messages**: Don't expose sensitive information in error messages
6. **Rate Limiting**: Implement rate limiting for API calls
7. **CORS**: Configure CORS properly for your domain

## 🧪 Testing

### API Testing with Jest
```javascript
// api.test.js
import { loginUser, assessRisk } from './api';

describe('API Integration', () => {
  test('should login user successfully', async () => {
    const result = await loginUser('test@example.com', 'password123');
    expect(result.success).toBe(true);
    expect(result.data).toHaveProperty('access_token');
  });

  test('should assess risk successfully', async () => {
    const behaviorData = {
      typing_speed: 100,
      mouse_distance: 500,
      click_count: 10,
      session_duration: 120
    };
    
    const result = await assessRisk(behaviorData);
    expect(result).toHaveProperty('risk_label');
    expect(result).toHaveProperty('risk_score');
  });
});
```

## 📞 Support

If you encounter issues during integration:

1. **Check Backend Status**: Ensure the backend is running on `http://localhost:8000`
2. **Verify API Endpoints**: Test endpoints with curl or Postman
3. **Check CORS**: Ensure CORS is properly configured
4. **Review Error Logs**: Check browser console and backend logs
5. **Contact Backend Team**: For API-related issues

---

**Happy Coding! 🚀**

This integration guide should help you successfully integrate the Walmart Secure Backend with your frontend application. The backend provides robust authentication, behavioral biometrics, risk assessment, and analytics capabilities that you can leverage to build secure, user-friendly applications. 