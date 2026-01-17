// API Interceptor for FastAPI Backend
// Handles JWT token injection, error handling, and request/response interceptors

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { authClient } from '@/lib/auth-client';

// Create API client
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add JWT token
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    // Get session from Better Auth
    const session = await authClient.getSession();

    if (session?.accessToken) {
      config.headers.Authorization = `Bearer ${session.accessToken}`;
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    // Handle 401 Unauthorized - redirect to sign-in
    if (error.response?.status === 401) {
      // Save current location for return after sign-in
      const returnUrl = window.location.pathname;
      window.location.href = `/sign-in?returnUrl=${encodeURIComponent(returnUrl)}`;
    }

    // Handle other errors
    if (error.response?.status === 422) {
      // Validation error - let the calling code handle it
      return Promise.reject(error);
    }

    if (error.response?.status === 500) {
      // Server error - log and show generic message
      console.error('Server error:', error);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
