import PageLayout from "@/components/layouts/PageLayout";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { AssignmentDetailUpdateForm } from "@/types/assignment";
import { useForm, Controller } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { Search } from "lucide-react";
import { ConfirmationModal } from "@/components/UI/Modal";
import { useEffect, useState } from "react";
import SelectUserModalBody from "./SelectUserModalBody";
import SelectAssetModalBody from "./SelectAssetModalBody";
import { useSelectUserModalStore } from "@/stores/selectUserModalStore";
import { useSelectAssetModalStore } from "@/stores/selectAssetModalStore";
import { assignmentService } from "@/api/assignmentService";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";

interface DisplayNames {
    userName: string;
    assetName: string;
}

const defaultFormValues: AssignmentDetailUpdateForm = {
    assigned_to_id: 0,
    assigned_by_id: 0,
    asset_id: 0,
    assign_date: "",
    assignment_note: "",
};

export default function EditAssignment() {
    const { id } = useParams();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [isUserModalOpen, setIsUserModalOpen] = useState(false);
    const [isAssetModalOpen, setIsAssetModalOpen] = useState(false);
    const [displayNames, setDisplayNames] = useState<DisplayNames>({
        userName: "",
        assetName: "",
    });

    const {
        data: assignmentDetail,
        isLoading,
        error: queryError,
    } = useQuery({
        queryKey: ["assignment", id],
        queryFn: () => assignmentService.get_assignment_detail(Number(id)),
        enabled: !!id,
        refetchOnWindowFocus: false,
        refetchOnMount: false,
        gcTime: Infinity,
        staleTime: Infinity,
    });

    const {
        control,
        handleSubmit,
        formState: { isDirty },
        reset,
        setValue,
    } = useForm<AssignmentDetailUpdateForm>({
        defaultValues: defaultFormValues,
    });

    // const { selectedUser, reset: resetUserSelectionStore, setSelectedUser } = useSelectUserModalStore();
    // const { selectedAsset, reset: resetAssetSelectionStore, setSelectedAsset } = useSelectAssetModalStore();

    const { selectedUser, setSelectedUser } = useSelectUserModalStore();
    const { selectedAsset, setSelectedAsset } = useSelectAssetModalStore();

    // Initialize form with assignment data
    useEffect(() => {
        if (assignmentDetail?.data) {
            const { assignment, asset, assigned_to_user } = assignmentDetail.data;

            reset({
                assigned_to_id: assigned_to_user.id,
                assigned_by_id: assignment.assigned_by,
                asset_id: asset.id,
                assign_date: assignment.assign_date,
                assignment_note: assignment.assignment_note || "",
            });

            setDisplayNames({
                userName: `${assigned_to_user.first_name} ${assigned_to_user.last_name}`,
                assetName: asset.asset_name,
            });

            setSelectedUser({
                id: assigned_to_user.id,
                firstName: assigned_to_user.first_name,
                lastName: assigned_to_user.last_name,
            });

            setSelectedAsset({
                id: asset.id,
                assetCode: asset.asset_code,
                assetName: asset.asset_name,
                category: asset.category.category_name,
            });
        }
    }, [assignmentDetail, reset, setSelectedUser, setSelectedAsset]);

    useBreadcrumbs([
        {
            label: "Manage Assignment",
            path: "/manage-assignment",
        },
        {
            label: "Edit Assignment",
        },
    ]);

    const onSubmit = async (data: AssignmentDetailUpdateForm) => {
        if (!id) return;

        try {
            await assignmentService.update_assignment(Number(id), data);
            await queryClient.invalidateQueries({ queryKey: ["assignment", id] });
            toast({
                content: "Assignment updated successfully",
                alertType: "alert-success",
                duration: 3,
            });
        } catch (error) {
            const axiosError = error as AxiosError<{ detail: string }>;
            const errorMessage = axiosError.response?.data?.detail || "Failed to update assignment";
            toast({
                content: errorMessage,
                alertType: "alert-error",
                duration: 3,
            });
        }
    };

    const handleUserModalClose = () => {
        setIsUserModalOpen(false);
        // resetUserSelectionStore();
    };

    const handleUserModalSave = () => {
        if (selectedUser) {
            setValue("assigned_to_id", selectedUser.id, { shouldDirty: true });
            setDisplayNames((prev) => ({
                ...prev,
                userName: `${selectedUser.firstName} ${selectedUser.lastName}`,
            }));
        }
        handleUserModalClose();
    };

    const handleAssetModalClose = () => {
        setIsAssetModalOpen(false);
        // resetAssetSelectionStore();
    };

    const handleAssetModalSave = () => {
        if (selectedAsset) {
            setValue("asset_id", selectedAsset.id, { shouldDirty: true });
            setDisplayNames((prev) => ({
                ...prev,
                assetName: selectedAsset.assetName,
            }));
        }
        handleAssetModalClose();
    };

    if (isLoading) {
        return (
            <PageLayout title="Edit Assignment">
                <div className="flex justify-center items-center h-64">
                    <div className="loading loading-spinner loading-lg"></div>
                    <span className="ml-4">Loading assignment details...</span>
                </div>
            </PageLayout>
        );
    }

    if (queryError) {
        const error = queryError as AxiosError<{ detail: string }>;
        const is404 = error.response?.status === 404;
        const errorMessage =
            error.response?.data?.detail ||
            (is404
                ? "Assignment not found. The assignment might have been deleted or you don't have permission to access it."
                : "Error loading assignment details. Please try again.");

        return (
            <PageLayout title="Edit Assignment">
                <div className={`alert ${is404 ? "alert-warning" : "alert-error"}`}>
                    <span>{errorMessage}</span>
                </div>
            </PageLayout>
        );
    }

    if (!assignmentDetail) {
        return (
            <PageLayout title="Edit Assignment">
                <div className="alert alert-warning">
                    <span>No assignment data available.</span>
                </div>
            </PageLayout>
        );
    }

    return (
        <PageLayout title="Edit Assignment">
            <form className="max-w-md" onSubmit={handleSubmit(onSubmit)}>
                <div className="flex items-center mb-4 w-full">
                    <label className="w-1/4">User</label>
                    <div
                        className="flex grow border border-secondary rounded-sm p-2 cursor-pointer hover:bg-base-200 transition-colors"
                        onClick={() => setIsUserModalOpen(true)}
                    >
                        <div className="w-11/12">{displayNames.userName}</div>
                        <div className="w-1/12 flex items-center justify-center">
                            <Search className="text-base-content/50" />
                        </div>
                    </div>
                </div>

                <div className="flex items-center mb-4 w-full">
                    <label className="w-1/4">Asset</label>
                    <div
                        className="flex grow border border-secondary rounded-sm p-2 cursor-pointer hover:bg-base-200 transition-colors"
                        onClick={() => setIsAssetModalOpen(true)}
                    >
                        <div className="w-11/12">{displayNames.assetName}</div>
                        <div className="w-1/12 flex items-center justify-center">
                            <Search className="text-base-content/50" />
                        </div>
                    </div>
                </div>

                <div className="flex items-center mb-4 w-full">
                    <label className="w-1/4">Assigned Date</label>
                    <Controller
                        name="assign_date"
                        control={control}
                        rules={{ required: "Assigned date is required" }}
                        render={({ field, fieldState: { error } }) => (
                            <div className="grow">
                                <input
                                    type="date"
                                    className="input w-full rounded-sm p-2 border-secondary"
                                    {...field}
                                />
                                {error && <span className="text-error text-sm">{error.message}</span>}
                            </div>
                        )}
                    />
                </div>

                <div className="flex items-center mb-4 w-full">
                    <label className="w-1/4">Note</label>
                    <Controller
                        name="assignment_note"
                        control={control}
                        render={({ field }) => (
                            <textarea
                                className="textarea grow rounded-sm p-2 border-secondary"
                                placeholder="Enter note here..."
                                {...field}
                            />
                        )}
                    />
                </div>

                <div className="flex justify-end gap-4">
                    <button type="submit" className="btn btn-primary w-24" disabled={!isDirty}>
                        Save
                    </button>

                    <button type="button" className="btn btn-outline w-24" onClick={() => navigate(-1)}>
                        Cancel
                    </button>
                </div>
            </form>

            <ConfirmationModal
                isOpen={isUserModalOpen}
                onClose={handleUserModalClose}
                header="Select User"
                body={<SelectUserModalBody />}
                className="max-w-3/4"
                useBackdrop={false}
                confirmText="Save"
                cancelText="Cancel"
                callback={handleUserModalSave}
            />

            <ConfirmationModal
                isOpen={isAssetModalOpen}
                onClose={handleAssetModalClose}
                header="Select Asset"
                body={<SelectAssetModalBody />}
                className="max-w-3/4"
                useBackdrop={false}
                confirmText="Save"
                cancelText="Cancel"
                callback={handleAssetModalSave}
            />
        </PageLayout>
    );
}
