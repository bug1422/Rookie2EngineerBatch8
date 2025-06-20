import { ReactNode, useEffect, useRef } from 'react';
import { useAuthStore } from '@/stores/authStore';

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const initialize = useAuthStore(state => state.initialize);
    const loading = useAuthStore(state => state.loading);
    const hasInitialized = useRef(false);

    // Initialize auth state on mount, but only once
    useEffect(() => {
        if (!hasInitialized.current) {
            hasInitialized.current = true;
            initialize();
        }
    }, [initialize]);

    // Optional: You could add a loading indicator here
    if (loading) {
        return <div>Loading authentication...</div>; // Or your loading component
    }

    return <>{children}</>;
};
