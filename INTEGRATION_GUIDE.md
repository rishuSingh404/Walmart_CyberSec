# Walmart CyberSec Integration Guide

This document explains how the React web application has been integrated with your Flask API to provide comprehensive behavioral biometrics and security analysis.

## 🚀 Quick Start

### Prerequisites
1. **Flask Backend**: Ensure your Flask API is running on `http://localhost:5001`
2. **Node.js**: Version 16 or higher
3. **Dependencies**: All required packages are already installed

### Running the Application

**Option 1: Automated Startup (Recommended)**
```bash
# Windows - Run this in the project root
start_app.bat
```

**Option 2: Manual Startup**
```bash
# Terminal 1: Start Flask API
cd flask
start_flask.bat

# Terminal 2: Start React App
npm run dev
```

The application will be available at:
- **React Frontend**: http://localhost:5173
- **Flask API**: http://localhost:5001

## 🔧 Integration Overview

### 1. Behavioral Data Collection
- **File**: `src/utils/behaviorCollector.ts`
- **Purpose**: Collects real-time user behavioral metrics
- **Metrics Tracked**:
  - Typing speed and patterns
  - Mouse movement and distance
  - Click patterns
  - Scroll behavior
  - Session duration

### 2. Flask API Integration
- **File**: `src/utils/flaskApi.ts`
- **Purpose**: Handles all communication with your Flask backend
- **Endpoints Integrated**:
  - `/api/login` - Authentication with behavioral data
  - `/api/signup` - Registration with behavioral data
  - `/api/fingerprint/update` - Update behavioral fingerprint
  - `/api/fingerprint/analyze` - Detect behavioral anomalies
  - `/api/risk/assess` - Risk assessment
  - `/api/analytics/*` - Session and dashboard analytics
  - `/api/admin/*` - Admin endpoints

### 3. Authentication System
- **File**: `src/utils/auth.ts`
- **Changes**: Replaced Supabase with Flask API
- **Features**:
  - JWT token-based authentication
  - Automatic behavioral data collection during login
  - Token validation and refresh

### 4. Real-time Analytics
- **File**: `src/hooks/useFlaskAnalytics.ts`
- **Purpose**: Continuous behavioral monitoring and analysis
- **Features**:
  - Real-time risk assessment
  - Anomaly detection
  - Automatic alerts for suspicious behavior
  - Session analytics

## 📊 Dashboard Features

### Security Monitoring
- **Risk Score**: Real-time behavioral risk assessment
- **Behavior Status**: Anomaly detection with confidence levels
- **Session Metrics**: Duration, clicks, typing patterns
- **Security Stats**: Active sessions, high-risk counts, blocked attempts

### Manual Analysis
- **Current Metrics Display**: Real-time behavioral data
- **Manual Analysis Trigger**: Run comprehensive security analysis
- **Error Handling**: Clear feedback for API issues

## 🔐 Security Features

### 1. Behavioral Biometrics
```typescript
// Automatic collection during user interaction
const metrics = {
  typing_speed: 250.5,        // Milliseconds between keystrokes
  mouse_distance: 1200.75,    // Total mouse movement in pixels
  click_count: 5,             // Number of clicks
  typing_interval_variance: 0.2, // Typing pattern consistency
  session_duration: 15000.0,  // Session length in milliseconds
  scroll_depth: 0.75          // How far user scrolled (0-1)
}
```

### 2. Risk Assessment
- **ML-based scoring**: Uses your Flask model for risk calculation
- **Component scores**: Breakdown of risk factors
- **Adaptive thresholds**: Configurable risk levels
- **Real-time monitoring**: Continuous assessment during session

### 3. Anomaly Detection
- **Behavioral patterns**: Detects deviations from normal behavior
- **Confidence scoring**: Reliability of anomaly detection
- **Field-level analysis**: Identifies specific anomalous behaviors
- **Alert system**: Automatic notifications for suspicious activity

## 🛠️ Configuration

### Environment Variables
Create `.env` file in project root:
```env
VITE_FLASK_API_URL=http://localhost:5001
VITE_DEV_MODE=true
VITE_ANALYTICS_ENABLED=true
VITE_RISK_THRESHOLD=70
VITE_ANALYTICS_INTERVAL=30000
```

### API Configuration
The system automatically handles:
- Authentication headers
- Token refresh
- Error handling
- Request/response formatting

## 📱 User Experience

### Login Flow
1. User enters credentials
2. Behavioral data is collected automatically
3. Data is sent to Flask API with login request
4. Risk assessment is performed
5. User is authenticated or blocked based on risk

### Dashboard Experience
1. Real-time metrics display
2. Continuous behavioral monitoring
3. Security status indicators
4. Manual analysis tools
5. Admin controls (for admin users)

### Admin Panel
1. User management with risk levels
2. Audit logs from Flask API
3. System statistics
4. Security monitoring tools

## 🔧 Technical Details

### Data Flow
```
User Interaction → Behavior Collector → Flask API → Risk Assessment → UI Update
```

### Error Handling
- Network failures: Graceful degradation
- API errors: User-friendly messages
- Authentication: Automatic token refresh
- Rate limiting: Built-in retry logic

### Performance
- **Efficient collection**: Minimal impact on user experience
- **Optimized requests**: Batched API calls where possible
- **Caching**: Token and session data cached locally
- **Background processing**: Analytics run without blocking UI

## 🚨 Troubleshooting

### Common Issues

1. **Flask API not responding**
   - Check if Flask is running on port 5001
   - Verify environment variables
   - Check network connectivity

2. **Authentication failures**
   - Clear browser storage
   - Check token validity
   - Verify Flask API credentials

3. **Missing behavioral data**
   - Check browser console for errors
   - Verify event listeners are attached
   - Test with manual analysis

### Debug Tools
- Browser console logs
- Network tab for API calls
- Redux DevTools (if available)
- Flask API logs

## 📈 Monitoring

### Metrics to Watch
- **Risk scores**: Track average and peak values
- **Anomaly rates**: Monitor false positive rates
- **Session quality**: Ensure data collection is working
- **API performance**: Response times and error rates

### Alerts
- High risk scores (configurable threshold)
- Behavioral anomalies
- Failed authentication attempts
- API connectivity issues

## 🔄 Updates and Maintenance

### Adding New Features
1. Add endpoints to `flaskApi.ts`
2. Update types and interfaces
3. Implement UI components
4. Test with Flask backend

### Security Updates
1. Monitor for authentication issues
2. Update risk thresholds as needed
3. Review and update behavioral metrics
4. Test integration thoroughly

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask API logs
3. Test individual components
4. Contact the development team

## 🎯 Next Steps

### Recommended Enhancements
1. **Device Fingerprinting**: Add device-specific metrics
2. **Geolocation**: IP-based location verification
3. **Session Recording**: Detailed user interaction logs
4. **Machine Learning**: Enhanced pattern recognition
5. **Mobile Support**: Touch and accelerometer data

### Integration Testing
1. Test all authentication flows
2. Verify risk assessment accuracy
3. Check anomaly detection sensitivity
4. Performance testing under load
5. Security penetration testing

---

**Note**: This integration maintains your existing Flask API structure while providing a modern, secure frontend experience. All behavioral data collection is transparent to users and enhances security without impacting usability.
