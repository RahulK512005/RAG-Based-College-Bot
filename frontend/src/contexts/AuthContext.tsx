import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, AuthResponse } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string, confirm_password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check localStorage on mount
    const savedToken = localStorage.getItem('college_rag_token');
    const savedUser = localStorage.getItem('college_rag_user');

    if (savedToken && savedUser) {
      try {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('college_rag_token');
        localStorage.removeItem('college_rag_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await api.post<AuthResponse>('/auth/login', { email, password });
      const { access_token, user: userData } = res.data;
      
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('college_rag_token', access_token);
      localStorage.setItem('college_rag_user', JSON.stringify(userData));
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (name: string, email: string, password: string, confirm_password: string) => {
    setIsLoading(true);
    try {
      const res = await api.post<AuthResponse>('/auth/signup', {
        name,
        email,
        password,
        confirm_password
      });
      const { access_token, user: userData } = res.data;

      setToken(access_token);
      setUser(userData);
      localStorage.setItem('college_rag_token', access_token);
      localStorage.setItem('college_rag_user', JSON.stringify(userData));
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('college_rag_token');
    localStorage.removeItem('college_rag_user');
  };

  const isAuthenticated = !!token && !!user;
  const isAdmin = user?.role === 'admin';

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
        isAdmin,
        isLoading,
        login,
        signup,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
