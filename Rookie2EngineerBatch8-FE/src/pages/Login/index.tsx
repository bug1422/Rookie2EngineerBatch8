import SimpleNavbar from "@/components/UI/Navbar/SimpleNavbar";
import { FormEvent, useState, ChangeEvent } from "react";
import { useAuthStore } from "@/stores/authStore";
import { LoginRequest } from "@/types/auth";
import { Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";
import toast from "@/components/UI/Toast";
import "./login.css"; // Import the CSS file

export default function LoginPage() {
    const [formData, setFormData] = useState<LoginRequest & {error?: string}>({
        username: "",
        password: ""
    });
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false); // Add state for password visibility
    const login = useAuthStore(state => state.login);
    const navigate = useNavigate(); // Use React Router's navigation

    const isFormValid = formData.username.trim() !== "" && formData.password.trim() !== "";

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            await login(formData.username, formData.password);

            // Get the user state directly after login
            const user = useAuthStore.getState().user;

            // Check if user state is populated
            if (!user || !user.username) {
                setFormData(prev => ({
                    ...prev,
                    error: "Login successful but user data is missing. Please try again."
                }));
                return;
            }

            // Always navigate to home page
            // If it's first login, the Home component will show the password change modal
            // Only show a toast for successful regular logins
            if (!user.is_first_login) {
                toast({
                    content: "Login successful",
                    duration: 3,
                    alertType: "alert-success",
                });
            }

            // Navigate to home page in both cases
            navigate('/');
        } catch {
            // Show error message above the username
            setFormData(prev => ({
                ...prev,
                error: "Username or password is incorrect. Please try again"
            }));

        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-screen">
            <SimpleNavbar />
            <div className="flex-1 flex items-center justify-center ">
                <div className="flex flex-col border-1 border-neutral rounded-lg max-w-[500px] w-full mx-4 shadow-md overflow-hidden">
                    <div className="text-primary border-b border-neutral w-full text-center p-4 text-lg font-bold bg-base-300">
                        Welcome to Online Asset Management
                    </div>
                    <form onSubmit={handleSubmit} className="flex flex-col p-6">
                        {formData.error && (
                            <div className="text-error mb-4 p-2 bg-error/10 rounded-md">
                                {formData.error}
                            </div>
                        )}
                        <div className="flex flex-row items-center gap-4 mb-4">
                            <div className="flex flex-row items-center gap-1 w-32">
                                <label htmlFor="username" className="text-lg font-medium">
                                    Username
                                </label>
                                <span className="text-primary">*</span>
                            </div>
                            <input
                                type="text"
                                id="username"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className="input input-bordered flex-1"
                                required
                            />
                        </div>

                        <div className="flex flex-row items-center gap-4">
                            <div className="flex flex-row items-center gap-1 w-32">
                                <label htmlFor="password" className="text-lg font-medium">
                                    Password
                                </label>
                                <span className="text-primary">*</span>
                            </div>
                            <div className="relative flex-1">
                                <input
                                    type={showPassword ? "text" : "password"}
                                    id="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="input input-bordered w-full pr-10"
                                    required
                                />
                                <div
                                    className="absolute top-0 right-0 h-full w-10 flex items-center justify-center cursor-pointer z-10"
                                    onClick={() => setShowPassword(!showPassword)}
                                >
                                    {showPassword ?
                                        <EyeOff size={20} className="text-gray-500" /> :
                                        <Eye size={20} className="text-gray-500" />
                                    }
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-end mt-4">
                            <button
                                type="submit"
                                className="btn btn-primary px-8 w-24"
                                disabled={!isFormValid || isLoading}
                            >
                                {isLoading ? (
                                    <span className="loading loading-spinner loading-sm"></span>
                                ) : (
                                    "Login"
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
