import { Outlet, Navigate } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";

export default function ProtectedRoutes() {
    const { isAuthenticated, loading } = useAuthStore();
    
    // If still loading auth state, show loading component
    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div>Loading authentication...</div>
            </div>
        );
    }
    
    // Only redirect when we're sure authentication has failed
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}
