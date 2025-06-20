import { Modal } from "..";

interface ConfirmationModalPopUpProps {
  isOpen: boolean;
  setOpen: (open: boolean) => void;
  confirmationText?: string;
  onConfirm?: () => void;
}

export function ConfirmationModalPopUp({
  isOpen,
  setOpen,
  confirmationText,
  onConfirm,
}: ConfirmationModalPopUpProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={() => setOpen(false)}
      header={"Are you sure?"}
      body={
        <>
          <div className="py-3 text-center">
            {`Do you want to ${
              confirmationText
            } this ${confirmationText == "create a returning request for" ? "asset" : "assignment"}?`}
          </div>
          <div className="px-3 flex justify-center gap-3 my-3">
            <button
              className="btn btn-error p-5 capitalize"
              onClick={() => {
                onConfirm?.();
                setOpen(false);
              }}
            >
              {confirmationText == "create a returning request for" ? "Yes" : confirmationText}
            </button>
            <button
              className="btn p-5"
              onClick={() => {
                setOpen(false);
              }}
            >
              Cancel
            </button>
          </div>
        </>
      }
    />
  );
}
