// API Interceptor for FastAPI Backend
// Handles JWT token injection, error handling, and request/response interceptors

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { getJwtToken, clearJwtToken } from '@/lib/auth-client';

// Create API client
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add JWT token from localStorage
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get JWT token stored after sign-in
    const token = getJwtToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
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
    // Handle 401 Unauthorized - clear token and redirect to sign-in
    if (error.response?.status === 401) {
      // Clear invalid/expired token
      clearJwtToken();
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
