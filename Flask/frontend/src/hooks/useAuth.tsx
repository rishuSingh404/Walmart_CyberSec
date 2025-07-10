
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, AuthState } from '@/types/auth';
import { useToast } from '@/hooks/use-toast';
import { apiClient } from '@/utils/api'; // Import the new apiClient

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isLoading: true,
    isAuthenticated: false,
  });
  const { toast } = useToast();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userString = localStorage.getItem('user');

    if (token && userString) {
      try {
        const user: User = JSON.parse(userString);
        setState({
          user,
          token,
          isLoading: false,
          isAuthenticated: true,
        });
      } catch (error) {
        console.error('Failed to parse user from localStorage', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setState(prev => ({ ...prev, isLoading: false }));
      }
    } else {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const response = await apiClient.post('/api/login', { email, password });
      
      if (response.access_token && response.user_id && response.email && response.role) {
        const user: User = {
          id: response.user_id,
          email: response.email,
          role: response.role,
        };
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('user', JSON.stringify(user));
        setState({
          user: user,
          token: response.access_token,
          isLoading: false,
          isAuthenticated: true,
        });
        toast({
          title: "Login successful",
          description: "Welcome back!",
        });
      } else {
        throw new Error(response.message || 'Login failed: Incomplete data received.');
      }
    } catch (error: any) {
      setState(prev => ({ ...prev, isLoading: false }));
      toast({
        title: "Login failed",
        description: error.message || "Invalid credentials",
        variant: "destructive",
      });
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const response = await apiClient.post('/api/signup', { email, password });
      
      if (response.message === 'User created successfully') {
        toast({
          title: "Registration successful",
          description: "You can now log in.",
        });
      } else {
        throw new Error(response.message || 'Registration failed.');
      }
    } catch (error: any) {
      setState(prev => ({ ...prev, isLoading: false }));
      toast({
        title: "Registration failed",
        description: error.message || "Registration failed",
        variant: "destructive",
      });
      throw error;
    }
  };

  const logout = async () => {
    try {
      // No specific logout endpoint on Flask backend, just clear client-side token
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setState({
        user: null,
        token: null,
        isLoading: false,
        isAuthenticated: false,
      });
      toast({
        title: "Logged out",
        description: "You have been logged out successfully",
      });
    } catch (error: any) {
      toast({
        title: "Logout failed",
        description: error.message || "Logout failed",
        variant: "destructive",
      });
    }
  };

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
