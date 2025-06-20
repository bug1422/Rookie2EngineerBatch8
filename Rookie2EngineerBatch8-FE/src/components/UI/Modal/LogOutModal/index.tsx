import { ReactNode } from "react";
import { Modal } from "@/components/UI/Modal";
import { useAuthStore } from "@/stores/authStore";
import { useNavigate } from "react-router-dom";
import toast from "../../Toast";
import "./index.css";

interface LogOutModalProps {
  isOpen: boolean;
  onClose: () => void;
  text?: string | ReactNode;
}

const LogOutHeader = () => {
  return <div className="flex items-center gap-2">Are you sure?</div>;
};

const LogOutBody = ({
  text,
  onClose,
}: {
  text?: string | ReactNode | undefined;
  onClose?: () => void;
}) => {
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      toast({
        content: "You have been logged out successfully",
        duration: 3,
        alertType: "alert-success",
      });
      navigate("/login");
    } catch {
      // Force redirect to login if there's an error
      window.location.replace("/login");
    }
    onClose?.();
  };

  return (
    <>
      <div className="py-3">{text ?? "Do you want to log out?"}</div>
      <div className="px-3 flex justify-center gap-3 my-3">
        <button className="btn btn-error p-5" onClick={handleLogout}>
          Log Out
        </button>
        <button className="btn p-5" onClick={() => onClose?.()}>
          Cancel
        </button>
      </div>
    </>
  );
};

export function LogOutModal({
  isOpen,
  onClose,
  text,
  ...props
}: LogOutModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      header={<LogOutHeader />}
      body={<LogOutBody text={text} onClose={onClose} />}
      onClose={onClose}
      className="logout-modal"
      closeIconSize={0}
      {...props}
    />
  );
}
