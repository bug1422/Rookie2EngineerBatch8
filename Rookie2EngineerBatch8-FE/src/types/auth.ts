export type LoginRequest = {
    username: string;
    password: string;
};

export type ChangePasswordRequest = {
    old_password: string;
    new_password: string;
}

// Define the token payload structure to match backend
export interface TokenPayload {
    sub: string;  // username
    exp: number;  // expiry timestamp
    user_id: number;
}

export interface AccessTokenPayload extends TokenPayload {
    first_name: string;
    last_name: string;
    type: string;
    is_first_login: boolean;
    location: string;
}

export interface User {
    username?: string;
    userId?: number;
    firstName?: string;
    lastName?: string;
    type?: UserType;
    is_first_login?: boolean;
    location?: string;
}

export interface AuthState {
    isAuthenticated: boolean;
    user: User;
    loading: boolean;

    // Actions
    login: (username: string, password: string) => Promise<void>;
    change_password: (old_password: string, new_password: string) => Promise<void>;
    logout: () => Promise<void>;
    checkTokenExpiry: () => Promise<boolean>;
    refreshTokens: () => Promise<AccessTokenPayload>;
    parseToken: (token: string) => void;
    initialize: () => void;
    checkAuthState: () => boolean;
}

export const UserType = {
    ADMIN: "admin",
    STAFF: "staff",
} as const;

export type UserType = typeof UserType[keyof typeof UserType];