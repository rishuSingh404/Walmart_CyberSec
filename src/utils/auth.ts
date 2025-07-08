
import { AuthResponse, LoginCredentials, RegisterCredentials, User } from '@/types/auth';
import { authService } from '@/utils/flaskApi';
import { getBehaviorCollector } from '@/utils/behaviorCollector';

export const authUtils = {
  // Token management
  getToken: (): string | null => {
    return localStorage.getItem('auth_token');
  },

  setToken: (token: string): void => {
    localStorage.setItem('auth_token', token);
  },

  removeToken: (): void => {
    localStorage.removeItem('auth_token');
  },

  // JWT token validation
  isTokenValid: (token: string): boolean => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  },

  // Supabase API calls
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    // Get behavioral metrics
    const collector = getBehaviorCollector();
    const behaviorMetrics = collector.getMetrics();
    
    try {
      const response = await authService.login(
        credentials.email, 
        credentials.password, 
        behaviorMetrics
      );

      // Create user object from Flask response
      const user: User = {
        id: credentials.email, // Flask API doesn't return user ID, using email as ID
        email: credentials.email,
        name: credentials.email.split('@')[0], // Extract name from email
      };

      const token = response.access_token;
      authUtils.setToken(token);

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || error.message || 'Login failed');
    }
  },

  register: async (credentials: RegisterCredentials): Promise<AuthResponse> => {
    // Get behavioral metrics
    const collector = getBehaviorCollector();
    const behaviorMetrics = collector.getMetrics();
    
    try {
      const response = await authService.signup(
        credentials.email, 
        credentials.password, 
        behaviorMetrics
      );

      // Create user object from Flask response
      const user: User = {
        id: credentials.email, // Flask API doesn't return user ID, using email as ID
        email: credentials.email,
        name: credentials.name,
      };

      const token = response.access_token;
      authUtils.setToken(token);

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || error.message || 'Registration failed');
    }
  },

  logout: async (): Promise<void> => {
    authService.logout();
    authUtils.removeToken();
  },

  getCurrentUser: async (): Promise<User> => {
    const token = authUtils.getToken();
    
    if (!token || !authUtils.isTokenValid(token)) {
      throw new Error('User not authenticated');
    }

    // For Flask API, we'll decode the JWT token to get user info
    // or make a request to get current user info
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        id: payload.sub || payload.email || 'unknown',
        email: payload.email || 'unknown@example.com',
        name: payload.name || payload.email?.split('@')[0] || 'Unknown User',
      };
    } catch (error) {
      throw new Error('Invalid token format');
    }
  },
};
