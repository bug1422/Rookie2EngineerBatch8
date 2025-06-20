import { cn } from "@/utils/cn";
import { ReactNode } from "react";

/**
 * Props for the base Modal component
 */
interface ModalProps {
  /** Unique identifier for the modal */
  id?: string;

  /** Controls modal visibility
   * @default false
   */
  isOpen?: boolean;

  /** Content to display in modal header
   * @example
   * header="User Details"
   * // or
   * header={<CustomHeader />}
   */
  header: string | ReactNode;

  /** Content to display in modal body
   * @example
   * body="Simple text content"
   * // or
   * body={<UserDetailsForm />}
   */
  body: string | ReactNode;

  /** Additional CSS classes for styling
   * @example className="max-w-2xl"
   */
  className?: string;

  /** Size of the close icon in pixels
   * @default 24
   * @deprecated
   */
  closeIconSize?: number;

  /** Handler called when modal is closed
   * @example onClose={() => setIsOpen(false)}
   */
  onClose: () => void;
  /** Whether to use a close button in the header */
  useCloseButton?: boolean;
  /** Whether to enable close when clicking outside */
  useBackdrop?: boolean;
}

export function Modal({
  id,
  isOpen = false,
  header,
  body,
  className,
  // closeIconSize = 24,
  onClose,
  useCloseButton = true,
  useBackdrop = true,
}: ModalProps) {
  return (
    <dialog id={id} className={cn("modal", isOpen && "modal-open")}>
      <div className={cn("modal-box p-0 bg-transparent", className)}>
        <div className="flex rounded-t-md p-3 justify-between items-center bg-neutral-content">
          {typeof header == "string" ? (
            <div className="font-bold text-xl text-primary truncate pr-2 pl-8">
              {header}
            </div>
          ) : (
            <>{header}</>
          )}
          {useCloseButton && (
            <button
              className="btn btn-outline btn-square w-5 h-5 text-primary font-black p-2 border-4 hover:text-secondary/20"
              onClick={onClose}
            >
              X
            </button>
          )}
        </div>
        <div className="py-3 px-8 bg-white border-2 border-neutral-content rounded-b-md overflow-x-hidden">
          {body}
        </div>
      </div>
      {useBackdrop && <div className="modal-backdrop" onClick={onClose} />}
    </dialog>
  );
}

interface ConfirmationModalProps
  extends Partial<Omit<ModalProps, "isOpen" | "onClose">>,
    Pick<ModalProps, "isOpen" | "onClose"> {
  /** Callback function executed when user confirms action
   * @important onClose is automatically called after callback. Don't declare onClose again in the callback
   * @example callback={() => handleDeleteUser(id)}
   */
  callback?: () => void;
  confirmText?: string;
  cancelText?: string;
}
const ConfirmationHeader = () => {
  return <div>Are you sure?</div>;
};

const ConfirmationBody = ({
  body,
  callback,
  onClose,
  confirmText = "Yes",
  cancelText = "No",
}: Pick<ConfirmationModalProps, "body" | "callback" | "onClose" | "confirmText" | "cancelText">) => {
  return (
    <>
      <div className="py-3">
        {body ?? "Are you sure to continue this action?"}
      </div>
      <div className="px-3 flex justify-end gap-3 my-3">
        <div
          className="btn btn-primary p-5 "
          onClick={() => {
            callback?.();
            onClose?.();
          }}
        >
          {confirmText}
        </div>
        <div className="btn p-5" onClick={() => onClose?.()}>
          {cancelText}
        </div>
      </div>
    </>
  );
};

export function ConfirmationModal({
  header,
  body,
  callback,
  onClose,
  confirmText,
  cancelText,
  ...props
}: ConfirmationModalProps) {
  return (
    <Modal
      header={header ?? <ConfirmationHeader />}
      body={
        <ConfirmationBody body={body} callback={callback} onClose={onClose} confirmText={confirmText} cancelText={cancelText} />
      }
      onClose={onClose}
      {...props}
    />
  );
}
