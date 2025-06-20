import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import { useAuthStore } from '@/stores/authStore';

interface QueueItem {
  resolve: (value: unknown) => void;
  reject: (reason: unknown) => void;
}

interface ApiError {
  response?: {
    status: number;
    data: unknown;
  };
  message: string;
}

let isLoggingOut = false;
let isRefreshing = false;
let failedQueue: QueueItem[] = [];

const processQueue = (error: ApiError | null, token: string | null = null): void => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  
  failedQueue = [];
};

// Create axios instance
const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // This is important for CORS requests with credentials
  timeout: 10000, // Increased timeout for better reliability
});

// Request interceptor
axiosClient.interceptors.request.use(
  (config: import("axios").InternalAxiosRequestConfig) => {
    // Get isAuthenticated from the auth store
    const { isAuthenticated } = useAuthStore.getState();

    const isLoginRequest = config.url?.includes('/auth/login');
    const isRefreshRequest = config.url?.includes('/auth/refresh');
    const isLogoutRequest = config.url?.includes('/auth/logout');
    const isAuthCheckRequest = config.url?.includes('/auth/check');

    // If not authenticated and not trying to log in, refresh token, auth check, or log out,
    // redirect to login.
    if (!isAuthenticated && !isLoginRequest && !isRefreshRequest && !isLogoutRequest && !isAuthCheckRequest) {
      console.warn("User not authenticated (and not a login/refresh/logout/auth-check attempt). Redirecting to login.");
      // Call logout to ensure any cleanup is done, then redirect.
      useAuthStore.getState().logout(); 

      if (window.location.pathname !== '/login') {
        sessionStorage.setItem('redirectPath', window.location.pathname);
        window.location.replace('/login');
      }
      
      // Cancel the current request by throwing an error
      return Promise.reject(new axios.Cancel("Request cancelled due to missing authentication."));
    }

    if (config.withCredentials !== undefined) {
      config.withCredentials = true;
    }
    
    return config;
  },
  (error: AxiosError) => {
    console.error("Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor
axiosClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // Skip token refresh if we're logging out
    if (isLoggingOut) {
      return Promise.reject(error);
    }
    
    // Check if this is a request that shouldn't trigger token refresh
    const isLoginRequest = originalRequest.url?.includes('/auth/login');
    const isRefreshRequest = originalRequest.url?.includes('/auth/refresh');
    const isChangePasswordRequest = originalRequest.url?.includes('/auth/change-password');
    
    // Handle 400 errors on change password requests (validation errors)
    if (error.response?.status === 400 && isChangePasswordRequest) {
      return Promise.reject(error);
    }
    
    // Handle 401 errors for requests that should trigger token refresh
    if (error.response?.status === 401 && 
        !originalRequest._retry && 
        !isLoginRequest && 
        !isRefreshRequest) {
      
      
      // If already refreshing, queue this request
      if (isRefreshing) {
        return new Promise<AxiosResponse>((resolve, reject) => {
          failedQueue.push({ 
            resolve: (value: unknown) => resolve(value as AxiosResponse), 
            reject 
          });
        }).then(() => {
          return axiosClient(originalRequest);
        }).catch((err: AxiosError) => {
          return Promise.reject(err);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
            
      try {
        await useAuthStore.getState().refreshTokens();
        processQueue(null, 'success');
        return axiosClient(originalRequest);
      } catch (refreshError: unknown) {
        const apiError = refreshError as ApiError;
        processQueue(apiError, null);
        
        // Handle Redis unavailable error
        if (apiError?.response?.status === 503) {
          console.warn("Service temporarily unavailable during token refresh");
          return Promise.reject(error);
        }
        
        // For other errors, logout and redirect
        console.error("Token refresh failed:", refreshError);
        useAuthStore.getState().logout();
        
        if (window.location.pathname !== '/login') {
          sessionStorage.setItem('redirectPath', window.location.pathname);
          window.location.replace('/login');
        }
        
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    // Handle cases where CORS might block the response (e.g., no tokens at all)
    // leading to error.response being undefined and a generic "Network Error".
    if (!error.response && error.message === 'Network Error') {
      // Check if tokens are actually missing. If they are, it's likely our scenario.
      const { isAuthenticated } = useAuthStore.getState();
      const isChangePassword = originalRequest.url?.includes('/auth/change-password');

      // If it's a change password request failing with a network error (likely CORS on 401)
      // OR if genuinely not authenticated, then logout.
      if (isChangePassword || !isAuthenticated) {
        console.error("Network error, potentially due to missing tokens. Logging out. isChangePassword:", isChangePassword, "isAuthenticated:", isAuthenticated);
        useAuthStore.getState().logout();
        if (window.location.pathname !== '/login') {
          sessionStorage.setItem('redirectPath', window.location.pathname);
          window.location.replace('/login');
        }
        // Return a new promise that never resolves to prevent further processing of this error
        return new Promise(() => {}); 
      }
    }
    
    return Promise.reject(error);
  }
);

export default axiosClient;

export const setLoggingOut = (value: boolean): void => {
  isLoggingOut = value;
};
