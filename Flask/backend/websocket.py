from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
import logging
from datetime import datetime
import json

# Configure logging
logger = logging.getLogger(__name__)

# Global socketio instance
socketio = None

def init_socketio(app):
    """Initialize SocketIO with the Flask app."""
    global socketio
    
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode='threading',
        logger=True,
        engineio_logger=True
    )
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        logger.info(f"Client connected: {request.sid}")
        emit('status', {'message': 'Connected to server', 'timestamp': datetime.now().isoformat()})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info(f"Client disconnected: {request.sid}")
    
    @socketio.on('join_admin_room')
    def handle_join_admin_room(data):
        """Join admin room for real-time updates."""
        user_id = data.get('user_id')
        user_role = data.get('role')
        
        if user_role == 'admin':
            join_room('admin_room')
            emit('status', {'message': 'Joined admin room', 'timestamp': datetime.now().isoformat()})
            logger.info(f"Admin user {user_id} joined admin room")
        else:
            emit('error', {'message': 'Access denied to admin room'})
    
    @socketio.on('join_user_room')
    def handle_join_user_room(data):
        """Join user-specific room."""
        user_id = data.get('user_id')
        room_name = f'user_{user_id}'
        join_room(room_name)
        emit('status', {'message': f'Joined user room {room_name}', 'timestamp': datetime.now().isoformat()})
        logger.info(f"User {user_id} joined room {room_name}")
    
    @socketio.on('leave_room')
    def handle_leave_room(data):
        """Leave a specific room."""
        room_name = data.get('room')
        leave_room(room_name)
        emit('status', {'message': f'Left room {room_name}', 'timestamp': datetime.now().isoformat()})
    
    @socketio.on('request_analytics')
    def handle_request_analytics(data):
        """Handle analytics data requests."""
        user_id = data.get('user_id')
        user_role = data.get('role')
        
        if user_role == 'admin':
            # Emit analytics data to admin room
            emit('analytics_update', {
                'type': 'user_analytics',
                'data': {
                    'total_users': 150,
                    'active_users': 89,
                    'new_users_today': 12,
                    'login_success_rate': 94.5,
                    'timestamp': datetime.now().isoformat()
                }
            }, room='admin_room')
        else:
            # Emit user-specific analytics
            emit('analytics_update', {
                'type': 'user_analytics',
                'data': {
                    'user_id': user_id,
                    'session_duration': 1800,
                    'risk_score': 0.15,
                    'timestamp': datetime.now().isoformat()
                }
            }, room=f'user_{user_id}')
    
    @socketio.on('request_otp_attempts')
    def handle_request_otp_attempts(data):
        """Handle OTP attempts data requests."""
        user_role = data.get('role')
        
        if user_role == 'admin':
            # Emit OTP attempts data to admin room
            emit('otp_attempts_update', {
                'type': 'otp_attempts',
                'data': {
                    'total_attempts': 156,
                    'successful_attempts': 142,
                    'failed_attempts': 14,
                    'blocked_attempts': 2,
                    'timestamp': datetime.now().isoformat()
                }
            }, room='admin_room')
    
    @socketio.on('request_login_attempts')
    def handle_request_login_attempts(data):
        """Handle login attempts data requests."""
        user_role = data.get('role')
        
        if user_role == 'admin':
            # Emit login attempts data to admin room
            emit('login_attempts_update', {
                'type': 'login_attempts',
                'data': {
                    'total_attempts': 89,
                    'successful_attempts': 78,
                    'failed_attempts': 11,
                    'timestamp': datetime.now().isoformat()
                }
            }, room='admin_room')
    
    @socketio.on('request_risk_data')
    def handle_request_risk_data(data):
        """Handle risk assessment data requests."""
        user_role = data.get('role')
        
        if user_role == 'admin':
            # Emit risk data to admin room
            emit('risk_data_update', {
                'type': 'risk_data',
                'data': {
                    'low_risk': 65,
                    'medium_risk': 25,
                    'high_risk': 10,
                    'timestamp': datetime.now().isoformat()
                }
            }, room='admin_room')
    
    return socketio

def emit_to_admin(event, data):
    """Emit data to admin room."""
    if socketio:
        socketio.emit(event, data, room='admin_room')

def emit_to_user(user_id, event, data):
    """Emit data to specific user room."""
    if socketio:
        socketio.emit(event, data, room=f'user_{user_id}')

def emit_to_all(event, data):
    """Emit data to all connected clients."""
    if socketio:
        socketio.emit(event, data)

def broadcast_analytics_update(analytics_data):
    """Broadcast analytics update to admin room."""
    emit_to_admin('analytics_update', {
        'type': 'user_analytics',
        'data': analytics_data,
        'timestamp': datetime.now().isoformat()
    })

def broadcast_otp_update(otp_data):
    """Broadcast OTP update to admin room."""
    emit_to_admin('otp_attempts_update', {
        'type': 'otp_attempts',
        'data': otp_data,
        'timestamp': datetime.now().isoformat()
    })

def broadcast_login_update(login_data):
    """Broadcast login update to admin room."""
    emit_to_admin('login_attempts_update', {
        'type': 'login_attempts',
        'data': login_data,
        'timestamp': datetime.now().isoformat()
    })

def broadcast_risk_update(risk_data):
    """Broadcast risk update to admin room."""
    emit_to_admin('risk_data_update', {
        'type': 'risk_data',
        'data': risk_data,
        'timestamp': datetime.now().isoformat()
    }) 