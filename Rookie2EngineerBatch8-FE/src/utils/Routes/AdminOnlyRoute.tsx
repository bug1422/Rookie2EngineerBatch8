import { Outlet } from "react-router-dom";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import { Type } from "@/types/enums";

export function AdminOnlyRoute() {
    const userType = useAuthStore(state => state.user.type);
    if (userType === Type.ADMIN) {
        return <Outlet />;
    }
    return <Navigate to="/" />;
}