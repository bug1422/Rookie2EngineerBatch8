import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { jwtDecode } from "jwt-decode";
import { authService } from "@/api/authService";
import { AccessTokenPayload, AuthState, User, UserType } from "@/types/auth";
import { Location } from "@/types/enums";
import { setLoggingOut } from "@/api/axiosClient";
import Cookies from "js-cookie";
import axiosClient from "@/api/axiosClient";

// Helper function to map location value from backend to frontend enum
const mapLocationValue = (locationValue: string): string => {
  // Map the location value from the backend (e.g., "Ho Chi Minh") to the frontend enum key (e.g., "HCM")
  if (locationValue === "Ho Chi Minh") return Location.HCM;
  if (locationValue === "Hanoi") return Location.HANOI;
  if (locationValue === "Danang") return Location.DANANG;

  // If no match is found, return the original value
  console.warn(`Unknown location value: ${locationValue}`);
  return locationValue;
};

const defaultUser: User = {};

const clearLegacyCookies = () => {
  
  // Remove with js-cookie
  Cookies.remove('access_token', { path: '/' });
  Cookies.remove('refresh_token', { path: '/' });
  
  // Remove with document.cookie for various domain/path combinations
  const cookiesToClear = ['access_token', 'refresh_token'];
  const pathsToTry = ['/', ''];
  const domainsToTry = [
    undefined,
    window.location.hostname,
    `.${window.location.hostname}`,
    'localhost',
    '.localhost'
  ];
  
  cookiesToClear.forEach(cookieName => {
    pathsToTry.forEach(path => {
      domainsToTry.forEach(domain => {
        // Try with domain
        if (domain) {
          document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path}; domain=${domain};`;
        } else {
          document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path};`;
        }
      });
    });
  });
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: defaultUser,
      loading: true,
      isAuthenticated: false,

      // Helper function to check if auth state is consistent with cookies
      checkAuthState: () => {
        const { isAuthenticated } = get();
        return isAuthenticated;
      },

      parseToken: (token: string) => {
        try {
          const decoded = jwtDecode<AccessTokenPayload>(token);
          set({
            isAuthenticated: true,
            user: {
              username: decoded.sub,
              userId: decoded.user_id,
              firstName: decoded.first_name,
              lastName: decoded.last_name,
              type: decoded.type as UserType,
              is_first_login: decoded.is_first_login,
              location: mapLocationValue(decoded.location),
            },
          });
        } catch (error) {
          console.error("Error decoding token:", error);
          set({
            isAuthenticated: false,
            user: defaultUser,
          });
        }
      },

      initialize: () => {        
        clearLegacyCookies();

        const isOnLoginPage = window.location.pathname === '/login' || 
                             window.location.pathname.endsWith('/login');
        
        if (isOnLoginPage) {
          set({
            isAuthenticated: false,
            user: defaultUser,
            loading: false,
          });
          return;
        }

        // ALWAYS verify with server, regardless of persisted state
        set({ loading: true });

        get()
          .checkTokenExpiry()
          .then(() => {
            set({ 
              isAuthenticated: true,
              loading: false 
            });
          })
          .catch(() => {
            set({
              isAuthenticated: false,
              user: defaultUser,
              loading: false,
            });
          });
      },

      login: async (username: string, password: string) => {
        try {
          const response = await authService.login({ username, password });
          const { access_token } = response.data;

          // Parse token to get user data and update state
          const decoded = jwtDecode<AccessTokenPayload>(access_token);

          // Update state with user data from token
          set({
            isAuthenticated: true,
            loading: false,
            user: {
              username: decoded.sub,
              userId: decoded.user_id,
              firstName: decoded.first_name,
              lastName: decoded.last_name,
              type: decoded.type as UserType,
              is_first_login: decoded.is_first_login,
              location: mapLocationValue(decoded.location),
            },
          });

        } catch (error) {
          console.error("Login error:", error);
          throw error;
        }
      },

      change_password: async (old_password: string, new_password: string) => {

        // Let axios interceptor handle 401 errors automatically
        const response = await authService.change_password({ old_password, new_password });
        console.log("Change password successful:", response.data);

        // After successful password change, refresh the token to get updated user state
        try {
          await get().refreshTokens();
        } catch (refreshError: unknown) {
          const apiError = refreshError as { response?: { status: number } };
          console.error("Failed to refresh token after password change:", refreshError);

          // Check if the error is a 503 Service Unavailable (Redis down)
          if (apiError?.response?.status === 503) {
            console.warn("Redis service unavailable during token refresh after password change. Updating local state only.");
          }

          // Even if token refresh fails, update local state
          set(state => ({
            ...state,
            user: {
              ...state.user,
              is_first_login: false
            }
          }));
        }
      },

      logout: async () => {
        setLoggingOut(true);
        
        try {
          if (window.location.pathname !== '/login') {
            window.location.replace('/login');
          }
          await authService.logout();

          set({
            isAuthenticated: false,
            user: defaultUser,
          });

        } catch {
          set({
            isAuthenticated: false,
            user: defaultUser,
          });

          if (window.location.pathname !== '/login') {
            window.location.replace('/login');
          }
        } finally {
          setLoggingOut(false);
        }
      },

      refreshTokens: async () => {
        try {
          const response = await authService.refreshToken();
          const { access_token } = response.data;

          const decoded = jwtDecode<AccessTokenPayload>(access_token);

          set({
            isAuthenticated: true,
            user: {
              username: decoded.sub,
              userId: decoded.user_id,
              firstName: decoded.first_name,
              lastName: decoded.last_name,
              type: decoded.type as UserType,
              is_first_login: decoded.is_first_login,
              location: mapLocationValue(decoded.location),
            },
          });
          return decoded;
        } catch (error: unknown) {
          console.error("Token refresh error:", error);

          if (error && typeof error === 'object' && 'response' in error && 
              error.response && typeof error.response === 'object' && 
              'status' in error.response && error.response.status === 503) {
            console.warn("Redis service unavailable during token refresh. Maintaining current auth state.");
            throw error;
          }

          set({
            isAuthenticated: false,
            user: defaultUser,
          });
          throw error;
        }
      },

      checkAuthStatus: async () => {
        try {
          // Make a simple request that requires authentication
          // This will automatically use HTTP-only cookies
          const response = await axiosClient.get('/v1/auth/me', {
            withCredentials: true
          });
          return response.data;
        } catch {
          return null;
        }
      },

      checkTokenExpiry: async () => {
        try {
          const response = await axiosClient.get('/v1/auth/check', {
            withCredentials: true,
          });
          if (response.status === 200) {
            return true;
          }
          return false;
        } catch (error) {
          console.error("Token expiry check failed:", error);
          return true;
        }
      }
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user, // Only persist user data, not isAuthenticated
      }),
    }
  )
);
