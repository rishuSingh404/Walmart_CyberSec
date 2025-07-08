
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, AuthState } from '@/types/auth';
import { authUtils } from '@/utils/auth';
import { useToast } from '@/hooks/use-toast';
import { getBehaviorCollector } from '@/utils/behaviorCollector';

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
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
    // Initialize behavior collector
    getBehaviorCollector();
    
    // Check for existing token on mount
    const initializeAuth = async () => {
      const token = authUtils.getToken();
      
      if (token && authUtils.isTokenValid(token)) {
        try {
          const user = await authUtils.getCurrentUser();
          setState({
            user,
            token,
            isLoading: false,
            isAuthenticated: true,
          });
        } catch (error) {
          // Invalid token, remove it
          authUtils.removeToken();
          setState(prev => ({ ...prev, isLoading: false }));
        }
      } else {
        // No valid token
        authUtils.removeToken();
        setState(prev => ({ ...prev, isLoading: false }));
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const { user, token } = await authUtils.login({ email, password });
      
      setState({
        user,
        token,
        isLoading: false,
        isAuthenticated: true,
      });
      
      toast({
        title: "Login successful",
        description: "Welcome back!",
      });
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

  const register = async (email: string, password: string, name: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const { user, token } = await authUtils.register({ email, password, name });
      
      setState({
        user,
        token,
        isLoading: false,
        isAuthenticated: true,
      });
      
      toast({
        title: "Registration successful",
        description: "Welcome! You are now logged in.",
      });
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
      await authUtils.logout();
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
