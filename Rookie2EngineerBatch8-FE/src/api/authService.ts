import axiosClient from "./axiosClient";
import { ChangePasswordRequest, LoginRequest } from "@/types/auth";
import { useAuthStore } from "@/stores/authStore";

const API_BASE_ROUTE = "/v1/auth";

export const authService = {
    login: (data: LoginRequest) => {
        // Create FormData object to match OAuth2PasswordRequestForm
        const formData = new FormData();
        formData.append('username', data.username);
        formData.append('password', data.password);

        return axiosClient.post(`${API_BASE_ROUTE}/login`, formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            withCredentials: true
        }).then(response => {

            return response;
        });
    },

    change_password: (data: ChangePasswordRequest) => {
        // Make the request with explicit headers
        return axiosClient.post(`${API_BASE_ROUTE}/change-password`, data, {
            headers: {
                'Content-Type': 'application/json',
            },
            // Ensure withCredentials is true to send cookies with the request
            withCredentials: true
        })
        .then(response => {
            return response;
        })
        .catch(error => {
            console.error("Change password error:", error.response?.data || error.message);
            throw error;
        });
    },

    refreshToken: () => {
        // Send empty body since backend will get refresh token from cookies
        return axiosClient.post(`${API_BASE_ROUTE}/refresh`, {}, {
            withCredentials: true
        })
        .then(response => {
            // Log the response tokens for debugging purposes only
        
            // Don't store tokens manually - rely on HTTP-only cookies set by backend
            return response;
        });
    },

    logout: () => {
        // Get current user ID for request
        const userId = useAuthStore.getState().user.userId;

        // Call logout endpoint to also remove cookies server-side
        // Send user ID in the request body to help server identify the user
        return axiosClient.post(`${API_BASE_ROUTE}/logout`, { user_id: userId }, {
            withCredentials: true
        })
        .then(response => {
            return response;
        })
        .catch(() => {
            // Even if API call fails, assume logout was successful
            return { data: { message: "Logged out locally" } };
        });
    }
};