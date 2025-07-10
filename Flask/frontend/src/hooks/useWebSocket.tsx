import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuth } from './useAuth';

interface WebSocketData {
  type: string;
  data: any;
  timestamp: string;
}

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<Socket | null>(null);
  const { user, isAuthenticated: authStatus } = useAuth();

  useEffect(() => {
    // Initialize SocketIO connection
    const socket = io('http://localhost:8000', {
      transports: ['websocket', 'polling'],
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    socketRef.current = socket;

    // Connection events
    socket.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      setError(null);
    });

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
      setIsAuthenticated(false);
    });

    socket.on('connect_error', (err) => {
      console.error('WebSocket connection error:', err);
      setError(`Connection error: ${err.message}`);
      setIsConnected(false);
    });

    // Status messages
    socket.on('status', (data) => {
      console.log('WebSocket status:', data);
    });

    // Error messages
    socket.on('error', (data) => {
      console.error('WebSocket error:', data);
      setError(data.message);
    });

    // Analytics updates
    socket.on('analytics_update', (data: WebSocketData) => {
      console.log('Analytics update received:', data);
      setLastMessage(data);
    });

    // OTP attempts updates
    socket.on('otp_attempts_update', (data: WebSocketData) => {
      console.log('OTP attempts update received:', data);
      setLastMessage(data);
    });

    // Login attempts updates
    socket.on('login_attempts_update', (data: WebSocketData) => {
      console.log('Login attempts update received:', data);
      setLastMessage(data);
    });

    // Risk data updates
    socket.on('risk_data_update', (data: WebSocketData) => {
      console.log('Risk data update received:', data);
      setLastMessage(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Join admin room when user is authenticated and is admin
  useEffect(() => {
    if (socketRef.current && authStatus && user?.role === 'admin') {
      socketRef.current.emit('join_admin_room', {
        user_id: user.id,
        role: user.role
      });
      setIsAuthenticated(true);
      console.log('Joined admin room');
    }
  }, [authStatus, user]);

  // Join user room when user is authenticated
  useEffect(() => {
    if (socketRef.current && authStatus && user) {
      socketRef.current.emit('join_user_room', {
        user_id: user.id,
        role: user.role
      });
      setIsAuthenticated(true);
      console.log('Joined user room');
    }
  }, [authStatus, user]);

  const requestAnalytics = () => {
    if (socketRef.current && authStatus && user) {
      socketRef.current.emit('request_analytics', {
        user_id: user.id,
        role: user.role
      });
    }
  };

  const requestOtpAttempts = () => {
    if (socketRef.current && authStatus && user) {
      socketRef.current.emit('request_otp_attempts', {
        user_id: user.id,
        role: user.role
      });
    }
  };

  const requestLoginAttempts = () => {
    if (socketRef.current && authStatus && user) {
      socketRef.current.emit('request_login_attempts', {
        user_id: user.id,
        role: user.role
      });
    }
  };

  const requestRiskData = () => {
    if (socketRef.current && authStatus && user) {
      socketRef.current.emit('request_risk_data', {
        user_id: user.id,
        role: user.role
      });
    }
  };

  const leaveRoom = (roomName: string) => {
    if (socketRef.current) {
      socketRef.current.emit('leave_room', { room: roomName });
    }
  };

  return {
    isConnected,
    isAuthenticated,
    lastMessage,
    error,
    requestAnalytics,
    requestOtpAttempts,
    requestLoginAttempts,
    requestRiskData,
    leaveRoom,
  };
}; 