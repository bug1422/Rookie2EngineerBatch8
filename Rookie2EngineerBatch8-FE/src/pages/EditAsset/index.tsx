import { assetService } from "@/api/assetService";
import PageLayout from "@/components/layouts/PageLayout";
import toast from "@/components/UI/Toast";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useAssetListQueryStore } from "@/stores/assetListQueryStore";
import { AssetUpdate, AssetUpdatableStates } from "@/types/asset";
import { AssetSortOption, SortDirection } from "@/types/enums";
import { useQuery } from "@tanstack/react-query";
import { Loader } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";

interface AssetFormProps extends AssetUpdate {
  category: string;
}

export default function EditAsset() {
  useBreadcrumbs([
    { label: "Manage Asset", path: "/manage-asset" },
    { label: "Edit Asset", path: "" },
  ]);
  const { setSortBy, setSortDirection } = useAssetListQueryStore();
  const navigate = useNavigate();

  // Form state
  const {
    formState: { errors, isValid, isLoading },
    handleSubmit,
    register,
    reset,
  } = useForm<AssetFormProps>({
    mode: "onChange",
  });
  const onSubmit = async (data: AssetFormProps) => {
    try {
      const updatedAsset: AssetUpdate = {
        asset_name: data.asset_name,
        specification: data.specification,
        installed_date: data.installed_date,
        asset_state: data.asset_state,
      };
      const response = await assetService.update_asset(assetId, updatedAsset);
      if (response.data) {
        toast({
          content: "Asset updated successfully",
          alertType: "alert-success",
          duration: 3,
        });
        setSortBy(AssetSortOption.UPDATED_DATE);
        setSortDirection(SortDirection.DESC);
        navigate("/manage-asset");
      }
    } catch {
      toast({
        content: "Failed to update asset",
        alertType: "alert-error",
        duration: 3,
      });
    }
  };

  const { id } = useParams<{ id: string }>();
  const assetId = Number(id);
  const fetchAssetDetail = async () => {
    try {
      const response = await assetService.get_asset(assetId);
      return response.data;
    } catch {
      return undefined;
    }
  };

  const { data: assetDetail } = useQuery({
    queryKey: ["edit-asset"],
    queryFn: () => fetchAssetDetail(),
    enabled: !!assetId,
  });

  useEffect(() => {
    if (assetDetail) {
      reset({
        asset_name: assetDetail.asset_name,
        category: assetDetail.category.category_name,
        specification: assetDetail.specification,
        installed_date: assetDetail.installed_date,
        asset_state: assetDetail.asset_state,
      });
    }
  }, [assetDetail]);

  return (
    <PageLayout title="Edit Asset">
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md">
        <div className="flex items-center mb-4">
          <label htmlFor="asset_name" className="w-1/4">
            Name
          </label>
          <div className="flex flex-col w-3/4">
            <input
              id="asset_name"
              type="text"
              className="input"
              {...register("asset_name", {
                required: true,
              })}
            />
            {errors.asset_name?.type === "required" && (
              <p className="textarea-xs text-error">Asset name is required</p>
            )}
          </div>
        </div>
        <div className="flex items-center mb-4">
          <label htmlFor="category" className="w-1/4">
            Category
          </label>
          <div className="flex flex-col w-3/4">
            <select
              disabled
              {...register("category", {
                required: true,
              })}
              id="category"
              className="select"
            >
              <option value={assetDetail?.category.category_name}>
                {assetDetail?.category.category_name}
              </option>
            </select>
            {errors.category?.type === "required" && (
              <p className="textarea-xs text-error">Category is required</p>
            )}
          </div>
        </div>
        <div className="flex items-start mb-4">
          <label className="w-1/4">Specification</label>
          <div className="flex flex-col w-3/4">
            <textarea
              id="asset_name"
              className="textarea"
              {...register("specification")}
            />
          </div>
        </div>
        <div className="flex items-center mb-4">
          <label className="w-1/4">Installed Date</label>
          <div className="flex flex-col w-3/4">
            <input
              id="installed_date"
              type="date"
              className="input"
              max={new Date().toISOString().split("T")[0]}
              {...register("installed_date", {
                required: true,
                validate: (value) => {
                  const selectedDate = new Date(value);
                  const today = new Date();
                  // clear time portion
                  selectedDate.setHours(0, 0, 0, 0);
                  today.setHours(0, 0, 0, 0);

                  return selectedDate <= today;
                },
              })}
            />
            {errors.installed_date?.type === "required" && (
              <p className="textarea-xs text-error">
                Installed Date is required
              </p>
            )}
            {errors.installed_date?.type === "validate" && (
              <p className="textare-xs text-error">
                Date cannot be in the future
              </p>
            )}
          </div>
        </div>
        <div className="flex items-start mb-4">
          <label className="w-1/4">State</label>
          <div className="w-3/4">
            {Object.values(AssetUpdatableStates).map((state) => (
              <div className="flex items-center gap-2" key={state as string}>
                <input
                  id={`radio-state-${state}`}
                  type="radio"
                  className="radio radio-sm radio-primary"
                  value={state}
                  {...register("asset_state")}
                />
                <label htmlFor={`radio-state-${state}`}>
                  {state as string}
                </label>
              </div>
            ))}
          </div>
        </div>
        <div className="flex justify-end gap-4">
          {isLoading ? (
            <div className="btn btn-outline">
              <Loader className="animate-spin" />
            </div>
          ) : (
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!isValid}
            >
              Save
            </button>
          )}

          <Link to="/manage-asset" className="btn btn-secondary btn-outline">
            Cancel
          </Link>
        </div>
      </form>
    </PageLayout>
  );
}
