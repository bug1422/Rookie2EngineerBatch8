import { Modal } from "@/components/UI/Modal";
import { useState, ReactNode } from "react";
import { assetService } from "@/api/assetService";
import toast from "@/components/UI/Toast";
import { useFetchClickedAsset } from "../AssetDisableModal/fetchClickedAsset";

interface AssetDisableModalProps {
  assetId: number;
  assetName?: string;
  children: ReactNode;
  validMessage?: string;
  invalidMessage?: string;
  className?: string;
  modalClassName?: string;
  callback?: () => void;
}

const DisableAssetHeader = () => {
  return <div className="flex items-center gap-2">Are you sure?</div>;
};

const DisableAssetBody = ({
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
        {message ?? "Do you want to disable this asset?"}
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

export default function AssetDisableModal({
  assetId,
  assetName,
  children,
  validMessage,
  invalidMessage,
  className,
  modalClassName,
  callback,
}: AssetDisableModalProps) {
  const [isOpen, setIsOpen] = useState(false);

  // Use the hook and destructure the necessary values
  const { data: assetData, refetch } = useFetchClickedAsset(assetId);

  const handleOnclick = async () => {
    setIsOpen(true);
    await refetch();
  };

  const handleDeleteAsset = async () => {
    try {
      const response = await assetService.delete_asset(assetId);
      if (response) {
        setIsOpen(false);
        toast({
          content: `Asset ${assetName} has been deleted successfully`,
          alertType: "alert-success",
          duration: 1,
        });
        callback?.();
      }
    } catch (error) {
      console.error("Error disabling asset:", error);
      toast({
        content: "Failed to disable asset",
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
        isOpen={isOpen && assetData?.is_valid == true}
        header={<DisableAssetHeader />}
        body={
          <DisableAssetBody
            message={validMessage}
            onDisable={handleDeleteAsset}
            onCancel={() => setIsOpen(false)}
          />
        }
        onClose={() => setIsOpen(false)}
        className={modalClassName}
        closeIconSize={0}
      />

      <Modal
        isOpen={isOpen && assetData?.is_valid == false}
        header="Cannot delete asset"
        body={
          invalidMessage
        }
        onClose={() => setIsOpen(false)}
        className={modalClassName}
      />
    </>
  );
}
