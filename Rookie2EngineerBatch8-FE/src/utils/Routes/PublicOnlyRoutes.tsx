import { Outlet, Navigate } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";

export default function PublicOnlyRoutes() {
    const { isAuthenticated, loading } = useAuthStore();

    // If still loading auth state, show loading or return null
    if (loading) {
        return <div>Loading...</div>; // Or any loading component
    }

    // If authenticated, always redirect to home page
    // The Home component will handle showing the password change modal if needed
    if (isAuthenticated) {
        return <Navigate to="/" />;
    }

    // Only allow access when not authenticated
    return <Outlet />;
}