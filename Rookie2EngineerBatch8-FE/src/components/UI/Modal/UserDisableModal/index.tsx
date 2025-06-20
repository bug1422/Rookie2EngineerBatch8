import { Modal } from "@/components/UI/Modal";
import { useState, ReactNode } from "react";
import { userService } from "@/api/userService";
import toast from "@/components/UI/Toast";
import { useFetchUserById } from "@/hooks/useFetchUser";

interface UserDisableModalProps {
  userId: number;
  userName?: string;
  children: ReactNode;
  validMessage?: string;
  invalidMessage?: string;
  className?: string;
  modalClassName?: string;
  callback?: () => void;
}

const DisableUserHeader = () => {
  return <div className="flex items-center gap-2">Are you sure?</div>;
};

const DisableUserBody = ({
  message,
  onDisable,
  onCancel,
}: {
  message?: string | ReactNode;
  onDisable: () => void;
  onCancel: () => void;
}) => {
  return (
    <>
      <div className="py-3 text-center">
        {message ?? "Do you want to disable this user?"}
      </div>
      <div className="px-3 flex justify-center gap-3 my-3">
        <button className="btn btn-error p-5" onClick={onDisable}>
          Disable
        </button>
        <button className="btn p-5" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </>
  );
};

export default function UserDisableModal({
  userId,
  userName,
  children,
  validMessage,
  invalidMessage,
  className,
  modalClassName,
  callback,
}: UserDisableModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  // const [modalType, setModalType] = useState<"valid" | "invalid">("valid");

  // Use the hook and destructure the necessary values
  const { data: userData, refetch } = useFetchUserById(userId);

  const handleOnclick = async () => {
    setIsOpen(true);
    await refetch();
  };

  const handleDeleteUser = async () => {
    try {
      const response = await userService.delete_user(userId);
      if (response) {
        setIsOpen(false);
        toast({
          content: `User ${userName} has been disabled successfully`,
          alertType: "alert-success",
          duration: 1,
        });
        callback?.();
      }
    } catch (error) {
      console.error("Error disabling user:", error);
      // setModalType("invalid");
      toast({
        content: "Failed to disable user",
        alertType: "alert-error",
        duration: 1,
      });
    }
  };

  return (
    <>
      <div onClick={handleOnclick} className={className}>
        {children}
      </div>

      <Modal
        isOpen={isOpen && userData?.is_valid == true}
        header={<DisableUserHeader />}
        body={
          <DisableUserBody
            message={validMessage}
            onDisable={handleDeleteUser}
            onCancel={() => setIsOpen(false)}
          />
        }
        onClose={() => setIsOpen(false)}
        className={modalClassName}
        closeIconSize={0}
      />

      <Modal
        isOpen={isOpen && userData?.is_valid == false}
        header="Cannot disable user"
        body={
          invalidMessage
        }
        onClose={() => setIsOpen(false)}
        className={modalClassName}
      />
    </>
  );
}
