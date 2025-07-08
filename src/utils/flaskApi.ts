// Flask API Service for Walmart Secure Integration
import axios, { AxiosResponse } from 'axios';
import { BehaviorMetrics, RiskAssessmentMetrics } from '@/utils/behaviorCollector';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_FLASK_API_URL || 'http://localhost:5001';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types for API responses
export interface LoginRequest {
  email: string;
  password: string;
  behavior_metrics: BehaviorMetrics;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  behavior_metrics: BehaviorMetrics;
}

export interface AdminCheckResponse {
  is_admin: boolean;
}

export interface FingerprintUpdateResponse {
  status: string;
  message: string;
  confidence_score: number;
}

export interface FingerprintAnalysisResponse {
  is_anomaly: boolean;
  anomaly_score: number;
  confidence: number;
  anomalous_fields: string[];
}

export interface RiskAssessmentResponse {
  risk_score: number;
  risk_label: string;
  component_scores: {
    ml_score: number;
    fingerprint_diff: number;
    intent_score: number;
  };
}

export interface SessionAnalyticsResponse {
  session_id: string;
  start_time: string;
  duration: number;
  risk_level: string;
  events: any[];
}

export interface DashboardAnalyticsResponse {
  active_sessions: number;
  high_risk_count: number;
  login_attempts: number;
  blocked_attempts: number;
}

export interface User {
  id: string;
  email: string;
  risk_level: string;
}

export interface UsersResponse {
  users: User[];
}

export interface AuditLog {
  id: string;
  timestamp: string;
  user_id: string;
  action: string;
  details: any;
}

export interface AuditLogsResponse {
  logs: AuditLog[];
}

// Authentication Services
export const authService = {
  async login(email: string, password: string, behaviorMetrics: BehaviorMetrics): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await api.post('/api/login', {
      email,
      password,
      behavior_metrics: behaviorMetrics
    });
    
    // Store token
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    
    return response.data;
  },

  async signup(email: string, password: string, behaviorMetrics: BehaviorMetrics): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await api.post('/api/signup', {
      email,
      password,
      behavior_metrics: behaviorMetrics
    });
    
    // Store token
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    
    return response.data;
  },

  async checkAdmin(): Promise<AdminCheckResponse> {
    const response: AxiosResponse<AdminCheckResponse> = await api.get('/api/check-admin');
    return response.data;
  },

  logout(): void {
    localStorage.removeItem('auth_token');
  }
};

// Behavioral Biometrics Services
export const biometricsService = {
  async updateFingerprint(behaviorMetrics: BehaviorMetrics): Promise<FingerprintUpdateResponse> {
    const response: AxiosResponse<FingerprintUpdateResponse> = await api.post('/api/fingerprint/update', behaviorMetrics);
    return response.data;
  },

  async analyzeFingerprint(behaviorMetrics: BehaviorMetrics): Promise<FingerprintAnalysisResponse> {
    const response: AxiosResponse<FingerprintAnalysisResponse> = await api.post('/api/fingerprint/analyze', behaviorMetrics);
    return response.data;
  }
};

// Risk Assessment Services
export const riskService = {
  async assessRisk(metrics: RiskAssessmentMetrics): Promise<RiskAssessmentResponse> {
    const response: AxiosResponse<RiskAssessmentResponse> = await api.post('/api/risk/assess', metrics);
    return response.data;
  }
};

// Analytics Services
export const analyticsService = {
  async getSessionAnalytics(): Promise<SessionAnalyticsResponse> {
    const response: AxiosResponse<SessionAnalyticsResponse> = await api.get('/api/analytics/session');
    return response.data;
  },

  async getDashboardAnalytics(): Promise<DashboardAnalyticsResponse> {
    const response: AxiosResponse<DashboardAnalyticsResponse> = await api.get('/api/analytics/dashboard');
    return response.data;
  }
};

// Admin Services
export const adminService = {
  async getUsers(): Promise<UsersResponse> {
    const response: AxiosResponse<UsersResponse> = await api.get('/api/admin/users');
    return response.data;
  },

  async getAuditLogs(params?: {
    start_date?: string;
    end_date?: string;
    user_id?: string;
  }): Promise<AuditLogsResponse> {
    const response: AxiosResponse<AuditLogsResponse> = await api.get('/api/admin/audit-logs', { params });
    return response.data;
  }
};

// Export the configured axios instance for custom requests
export { api };

// Health check function
export const healthCheck = async (): Promise<boolean> => {
  try {
    await api.get('/health', { timeout: 5000 });
    return true;
  } catch (error) {
    console.warn('Flask API health check failed:', error);
    return false;
  }
};
