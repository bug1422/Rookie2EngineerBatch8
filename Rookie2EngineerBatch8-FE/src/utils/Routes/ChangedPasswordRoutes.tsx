import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import ChangePasswordModal from "@/components/UI/Modal/ChangePasswordModal";

// This component no longer redirects users who haven't changed their password
// Instead, the Home component will show a modal for first-time users
export default function ChangedPasswordRoutes() {
    const { user } = useAuthStore();
    const [isFirstLoginModalOpen, setIsFirstLoginModalOpen] = useState(false);
    const [firstLoginErrorMessage, setFirstLoginErrorMessage] = useState<
    string | undefined
    >(undefined);

    useEffect(() => {
    if (user.is_first_login) {
    // Show the password change modal without any toast notification
    setIsFirstLoginModalOpen(true);
    } else if (isFirstLoginModalOpen) {
    // If user is no longer in first login state but modal is open,
    // it means they just successfully changed their password
    // Close the modal automatically
    setIsFirstLoginModalOpen(false);
    setFirstLoginErrorMessage(undefined);
    }
    }, [user.is_first_login, isFirstLoginModalOpen]);

    const handleModalClose = () => {
        // Check if user is still in first login state
        // This will be false if the password was just changed successfully
        const currentUserState = useAuthStore.getState().user;

        if (currentUserState.is_first_login) {
        // Set error message to display in the form instead of showing a toast
        setFirstLoginErrorMessage(
            "You must change your password before continuing"
        );
        return;
        }

        // If we get here, either:
        // 1. User has successfully changed their password (is_first_login is now false)
        // 2. User was not in first login state to begin with
        setIsFirstLoginModalOpen(false);
        // Clear any error message when closing the modal
        setFirstLoginErrorMessage(undefined);
    };


    return (
        <>
            <ChangePasswordModal
                isOpen={isFirstLoginModalOpen}
                onClose={handleModalClose}
                firstLoginErrorMessage={firstLoginErrorMessage}
                modalId="change-password" // Add unique ID
            />
            <Outlet />
        </>
    );
}