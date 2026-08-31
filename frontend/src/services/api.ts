import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

// Request interceptor: Attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('college_rag_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Extract user-friendly error messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('college_rag_token');
      localStorage.removeItem('college_rag_user');
    }

    // Friendly error detection for missing or unreachable backend API
    if (!error.response) {
      if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
        return Promise.reject(
          new Error('Backend API unreachable. Please configure VITE_API_BASE_URL in Vercel settings.')
        );
      }
      return Promise.reject(new Error('Cannot connect to backend server. Make sure it is running on port 8000.'));
    }

    if (error.response?.status === 404) {
      return Promise.reject(
        new Error('Backend API endpoint not found. Ensure VITE_API_BASE_URL ends with /api.')
      );
    }
    
    const message =
      error.response?.data?.error?.message ||
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred';
      
    return Promise.reject(new Error(message));
  }
);
