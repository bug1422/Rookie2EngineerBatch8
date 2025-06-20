import SimpleNavbar from "@/components/UI/Navbar/SimpleNavbar";
import { FormEvent, useState, ChangeEvent, useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import "../Login/login.css"; // Import the CSS file

export default function LoginPage() {
    const [formData, setFormData] = useState<{
        old_password: string;
        new_password: string;
        repeat_new_password: string;
        error?: string;
    }>({
        old_password: "",
        new_password: "",
        repeat_new_password: ""
    });
    const [isLoading, setIsLoading] = useState(false);
    // Separate state for each password field's visibility
    const [showOldPassword, setShowOldPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showRepeatPassword, setShowRepeatPassword] = useState(false);
    const navigate = useNavigate();

    // Get user state
    const user = useAuthStore(state => state.user);

    // Check for token availability and auth state
    const isAuthenticated = useAuthStore(state => state.isAuthenticated);

    const checkAuthState = useAuthStore(state => state.checkAuthState);

    useEffect(() => {
        // Check if auth state is consistent with cookies
        const isAuthValid = checkAuthState();

        if (!isAuthValid) {
            navigate('/login');
            return;
        }

        // If auth is valid but user is not in first login state, redirect to home
        if (user.userId && !user.is_first_login) {
            navigate('/');
            return;
        }

        // Check for token in cookies (redundant but kept for safety)
        const token = Cookies.get('access_token');
        if (!token) {
            // This shouldn't happen if checkAuthState is working correctly
            setFormData(prev => ({
                ...prev,
                error: "Authentication token is missing. Please log in again."
            }));
        }
    }, [isAuthenticated, user, navigate, checkAuthState]);

    const change_password = useAuthStore(state => state.change_password);

    const isFormValid =
        formData.old_password.trim() !== "" &&
        formData.new_password.trim() !== "" &&
        formData.new_password === formData.repeat_new_password;

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (formData.new_password !== formData.repeat_new_password) {
            setFormData(prev => ({
                ...prev,
                error: "New passwords do not match"
            }));
            return;
        }

        setIsLoading(true);

        try {
            // Check auth state consistency before proceeding
            const isAuthValid = checkAuthState();
            if (!isAuthValid) {
                throw new Error("Authentication is invalid. Please log in again.");
            }

            // Double-check token availability (should be redundant with checkAuthState)
            const token = Cookies.get('access_token');
            if (!token) {
                throw new Error("Authentication token is missing. Please log in again.");
            }

            // Call the change password function
            await change_password(formData.old_password, formData.new_password);

            // Update user state to reflect that it's no longer first login
            // Note: This is redundant as the change_password function already updates this
            // but we'll keep it for clarity and as a safeguard
            useAuthStore.setState(state => ({
                ...state,
                user: {
                    ...state.user,
                    is_first_login: false
                }
            }));

            // Redirect to home page using React Router
            navigate('/');
        } catch (err: unknown) {
            // Show detailed error message
            let errorMessage = "Old password is incorrect or new password is invalid";

            // Type guard to check if error has response property
            if (err && typeof err === 'object' && 'response' in err) {
                const axiosError = err as { response?: { data?: { detail?: string } } };
                if (axiosError.response?.data?.detail) {
                    errorMessage = axiosError.response.data.detail;
                }
            }

            // Show error message above the form
            setFormData(prev => ({
                ...prev,
                error: errorMessage
            }));

        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-screen">
            <SimpleNavbar />
            <div className="flex-1 flex items-center justify-center">
                <div className="flex flex-col border-1 border-neutral rounded-lg max-w-[500px] w-full mx-4 shadow-md">
                    <div className="text-primary border-b border-neutral w-full text-center p-4 text-lg font-bold bg-base-300">
                        This is your first login, please change your default password
                    </div>
                    <form onSubmit={handleSubmit} className="flex flex-col p-6">
                        {formData.error && (
                            <div className="text-error mb-4 p-2 bg-error/10 rounded-md">
                                {formData.error}
                            </div>
                        )}
                        <div className="flex flex-row items-center gap-4 mb-4">
                            <div className="flex flex-row items-center gap-1 w-32">
                                <label htmlFor="old_password" className="text-lg font-medium">
                                    Old Password
                                </label>
                                <span className="text-primary">*</span>
                            </div>
                            <div className="relative flex-1">
                                <input
                                    type={showOldPassword ? "text" : "password"}
                                    id="old_password"
                                    name="old_password"
                                    value={formData.old_password}
                                    onChange={handleChange}
                                    className="input input-bordered w-full pr-10"
                                    required
                                />
                                <div
                                    className="absolute top-0 right-0 h-full w-10 flex items-center justify-center cursor-pointer z-10"
                                    onClick={() => setShowOldPassword(!showOldPassword)}
                                >
                                    {showOldPassword ?
                                        <EyeOff size={20} className="text-gray-500" /> :
                                        <Eye size={20} className="text-gray-500" />
                                    }
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-row items-center gap-4 mb-4">
                            <div className="flex flex-row items-center gap-1 w-32">
                                <label htmlFor="new_password" className="text-lg font-medium">
                                    New Password
                                </label>
                                <span className="text-primary">*</span>
                            </div>
                            <div className="relative flex-1">
                                <input
                                    type={showNewPassword ? "text" : "password"}
                                    id="new_password"
                                    name="new_password"
                                    value={formData.new_password}
                                    onChange={handleChange}
                                    className="input input-bordered w-full pr-10"
                                    required
                                />
                                <div
                                    className="absolute top-0 right-0 h-full w-10 flex items-center justify-center cursor-pointer z-10"
                                    onClick={() => setShowNewPassword(!showNewPassword)}
                                >
                                    {showNewPassword ?
                                        <EyeOff size={20} className="text-gray-500" /> :
                                        <Eye size={20} className="text-gray-500" />
                                    }
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-row items-center gap-4">
                            <div className="flex flex-row items-center gap-1 w-32">
                                <label htmlFor="repeat_new_password" className="text-lg font-medium">
                                    Repeat New Password
                                </label>
                                <span className="text-primary">*</span>
                            </div>
                            <div className="relative flex-1">
                                <input
                                    type={showRepeatPassword ? "text" : "password"}
                                    id="repeat_new_password"
                                    name="repeat_new_password"
                                    value={formData.repeat_new_password}
                                    onChange={handleChange}
                                    className="input input-bordered w-full pr-10"
                                    required
                                />
                                <div
                                    className="absolute top-0 right-0 h-full w-10 flex items-center justify-center cursor-pointer z-10"
                                    onClick={() => setShowRepeatPassword(!showRepeatPassword)}
                                >
                                    {showRepeatPassword ?
                                        <EyeOff size={20} className="text-gray-500" /> :
                                        <Eye size={20} className="text-gray-500" />
                                    }
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-end mt-4">
                            <button
                                type="submit"
                                className="btn btn-primary px-8 w-48"
                                disabled={!isFormValid || isLoading}
                            >
                                {isLoading ? (
                                    <span className="loading loading-spinner loading-sm"></span>
                                ) : (
                                    "Change password"
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
