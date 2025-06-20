import { FormEvent, useState, ChangeEvent, useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Modal } from "..";
import toast from "../../Toast";

interface ChangePasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
  firstLoginErrorMessage?: string;
}
const ChangePasswordBody = ({
  onClose,
  firstLoginErrorMessage,
  modalId = "" // Add modalId prop with default empty string
}: {
  onClose: () => void;
  firstLoginErrorMessage?: string;
  modalId?: string; // Add this prop
}) => {
  const [formData, setFormData] = useState<{
    old_password: string;
    new_password: string;
    repeat_new_password: string;
    error?: string;
  }>({
    old_password: "",
    new_password: "",
    repeat_new_password: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showRepeatPassword, setShowRepeatPassword] = useState(false); // Add state for password visibility
  const navigate = useNavigate();

  // Get user state
  const user = useAuthStore((state) => state.user);

  // Check for token availability and auth state
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);


  useEffect(() => {
    // Only check the auth store state - don't check cookies
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    // Remove the cookie checking logic entirely
    // The HTTP-only cookies will be sent automatically with requests
  }, [isAuthenticated, navigate]);

  const change_password = useAuthStore((state) => state.change_password);

  const isFormValid =
    formData.old_password.trim() !== "" &&
    formData.new_password.trim() !== "" &&
    formData.new_password === formData.repeat_new_password;

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    console.log(name, value);
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (formData.new_password !== formData.repeat_new_password) {
      setFormData((prev) => ({
        ...prev,
        error: "New passwords do not match",
      }));
      return;
    }

    setIsLoading(true);

    try {
      // Remove the redundant auth checks
      // Just call the change password function - it will handle authentication
      await change_password(formData.old_password, formData.new_password);

      // Remove the redundant state update - change_password already handles this
      
      // Show success message
      toast({
        content: user.is_first_login
          ? "Password changed successfully. You can now use the application."
          : "Password changed successfully",
        duration: 3,
        alertType: "alert-success",
      });

      // Reset form
      setFormData({
        old_password: "",
        new_password: "",
        repeat_new_password: "",
        error: undefined,
      });

      // Close modal
      onClose();
    } catch (err: unknown) {
      let errorMessage = "Failed to change password";

      if (err && typeof err === "object" && "response" in err) {
        const axiosError = err as { response?: { data?: { detail?: string } } };
        if (axiosError.response?.data?.detail) {
          errorMessage = axiosError.response.data.detail;
        }
      }

      setFormData((prev) => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="flex flex-col p-6">
      {/* Display form error or first login error message */}
      {(formData.error || firstLoginErrorMessage) && (
        <div className="text-error mb-4 p-2 bg-error/10 rounded-md">
          {formData.error || firstLoginErrorMessage}
        </div>
      )}
      <div className="flex flex-row items-center gap-4 mb-4">
        <div className="flex flex-row items-center gap-1 w-32">
          <label htmlFor={`modal_old_password${modalId}`} className="text-lg font-medium">
            Old Password
          </label>
          <span className="text-primary">*</span>
        </div>
        <div className="relative flex-1">
          <input
            type={showOldPassword ? "text" : "password"}
            id={`modal_old_password${modalId}`}
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
            {showOldPassword ? (
              <EyeOff size={20} className="text-gray-500" />
            ) : (
              <Eye size={20} className="text-gray-500" />
            )}
          </div>
        </div>
      </div>

      <div className="flex flex-row items-center gap-4 mb-4">
        <div className="flex flex-row items-center gap-1 w-32">
          <label htmlFor={`modal_new_password${modalId}`} className="text-lg font-medium">
            New Password
          </label>
          <span className="text-primary">*</span>
        </div>
        <div className="relative flex-1">
          <input
            type={showNewPassword ? "text" : "password"}
            id={`modal_new_password${modalId}`}
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
            {showNewPassword ? (
              <EyeOff size={20} className="text-gray-500" />
            ) : (
              <Eye size={20} className="text-gray-500" />
            )}
          </div>
        </div>
      </div>

      <div className="flex flex-row items-center gap-4">
        <div className="flex flex-row items-center gap-1 w-32">
          <label htmlFor={`modal_repeat_new_password${modalId}`} className="text-lg font-medium">
            Repeat New Password
          </label>
          <span className="text-primary">*</span>
        </div>
        <div className="relative flex-1">
          <input
            type={showRepeatPassword ? "text" : "password"}
            id={`modal_repeat_new_password${modalId}`}
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
            {showRepeatPassword ? (
              <EyeOff size={20} className="text-gray-500" />
            ) : (
              <Eye size={20} className="text-gray-500" />
            )}
          </div>
        </div>
      </div>

      <div className="flex flex-row justify-end gap-4">
        <div className="flex justify-end mt-4">
          <button
            type="submit"
            className="btn btn-primary px-8 w-24"
            disabled={!isFormValid || isLoading}
          >
            {isLoading ? (
              <span className="loading loading-spinner loading-sm"></span>
            ) : (
              "Save"
            )}
          </button>
        </div>

        {!user.is_first_login && (
          <div className="flex justify-end mt-4">
            <button
              type="button"
              onClick={onClose}
              className="btn w-24"
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="loading loading-spinner loading-sm"></span>
              ) : (
                "Cancel"
              )}
            </button>
          </div>
        )}
      </div>
    </form>
  );
};
const ChangePasswordHeader = () => {
  const { user } = useAuthStore();

  return (
    <div className="text-primary w-full text-center p-4 text-lg font-bold">
      {user.is_first_login
        ? "First Login - Change Your Default Password"
        : "Change Password"}
    </div>
  );
};
export default function ChangePasswordModal({
  isOpen,
  onClose,
  firstLoginErrorMessage,
  modalId = "" // Add modalId prop with default empty string
}: ChangePasswordModalProps & { modalId?: string }) { // Add modalId to props
  return (
    <Modal
      isOpen={isOpen}
      body={<ChangePasswordBody onClose={onClose} firstLoginErrorMessage={firstLoginErrorMessage} modalId={modalId} />}
      header={<ChangePasswordHeader />}
      onClose={onClose}
    />
  );
}
