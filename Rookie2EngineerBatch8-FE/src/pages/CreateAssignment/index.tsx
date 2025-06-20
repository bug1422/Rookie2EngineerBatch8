import PageLayout from "@/components/layouts/PageLayout";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { AssignmentCreateForm } from "@/types/assignment";
import { useForm, Controller } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import { ConfirmationModal } from "@/components/UI/Modal";
import { useEffect, useState } from "react";
import SelectUserModalBody from "./SelectUserModalBody";
import SelectAssetModalBody from "./SelectAssetModalBody";
import { useSelectUserModalStore } from "@/stores/selectUserModalStore";
import { useSelectAssetModalStore } from "@/stores/selectAssetModalStore";
import { useAssignmentListQueryStore } from "@/stores/assignmentListQueryStore";
import { assignmentService } from "@/api/assignmentService";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";
import { AssignmentSortOption, SortDirection } from "@/types/enums";

interface DisplayNames {
    userName: string;
    assetName: string;
}

export default function CreateAssignment() {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [isUserModalOpen, setIsUserModalOpen] = useState(false);
    const [isAssetModalOpen, setIsAssetModalOpen] = useState(false);
    const [displayNames, setDisplayNames] = useState<DisplayNames>({
        userName: "",
        assetName: "",
    });

    const { selectedUser, reset: resetUserModal } = useSelectUserModalStore();
    const { selectedAsset, reset: resetAssetModal } = useSelectAssetModalStore();
    const { setSortBy, setSortDirection } = useAssignmentListQueryStore();

    const {
        control,
        handleSubmit,
        setValue,
        watch,
    } = useForm<AssignmentCreateForm>({
        mode: "onChange",
        defaultValues: {
            assigned_to_id: 0,
            asset_id: 0,
            assign_date: new Date().toISOString().split('T')[0], // Default to current date
            assignment_note: "",
        },
    });

    const watchedValues = watch();
    const isFormValid = watchedValues.assigned_to_id > 0 &&
                       watchedValues.asset_id > 0 &&
                       watchedValues.assign_date !== "";

    // Update form when user is selected
    useEffect(() => {
        if (selectedUser) {
            setValue("assigned_to_id", selectedUser.id);
            setDisplayNames(prev => ({
                ...prev,
                userName: `${selectedUser.firstName} ${selectedUser.lastName}`,
            }));
        }
    }, [selectedUser, setValue]);

    // Update form when asset is selected
    useEffect(() => {
        if (selectedAsset) {
            setValue("asset_id", selectedAsset.id);
            setDisplayNames(prev => ({
                ...prev,
                assetName: `${selectedAsset.assetName}`,
            }));
        }
    }, [selectedAsset, setValue]);

    useBreadcrumbs([
        {
            label: "Manage Assignment",
            path: "/manage-assignment",
        },
        {
            label: "Create New Assignment",
        },
    ]);

    const createMutation = useMutation({
        mutationFn: (data: AssignmentCreateForm) => assignmentService.create_assignment(data),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["assignment-list"],
                exact: false
            });
            toast({
                content: "Assignment created successfully",
                alertType: "alert-success",
                duration: 3,
            });

            // Ensure when navigating back, the list shows the new assignment on top
            setSortBy(AssignmentSortOption.ASSIGNED_DATE);
            setSortDirection(SortDirection.DESC);
            navigate(-1);
        },
        onError: (error: AxiosError<{ detail: string }>) => {
            const errorMessage = error.response?.data?.detail || "Failed to create assignment";
            toast({
                content: errorMessage,
                alertType: "alert-error",
                duration: 3,
            });
        },
    });

    const onSubmit = async (data: AssignmentCreateForm) => {
        createMutation.mutate(data);
    };

    const handleCancel = () => {
        navigate(-1);
    };

    const handleUserModalClose = () => {
        setIsUserModalOpen(false);
    };

    const handleAssetModalClose = () => {
        setIsAssetModalOpen(false);
    };

    const handleUserModalSave = () => {
        if (selectedUser) {
            setValue("assigned_to_id", selectedUser.id);
            setDisplayNames((prev) => ({
                ...prev,
                userName: `${selectedUser.firstName} ${selectedUser.lastName}`,
            }));
        }
        handleUserModalClose();
    };

    const handleAssetModalSave = () => {
        if (selectedAsset) {
            setValue("asset_id", selectedAsset.id);
            setDisplayNames((prev) => ({
                ...prev,
                assetName: `${selectedAsset.assetName}`,
            }));
        }
        handleAssetModalClose();
    };

    // Reset modal stores when component unmounts
    useEffect(() => {
        return () => {
            resetUserModal();
            resetAssetModal();
        };
    }, [resetUserModal, resetAssetModal]);

    return (
        <PageLayout title="Create New Assignment">
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
                        render={({ field }) => (
                            <input
                                type="date"
                                className="input grow rounded-sm p-2 border-secondary"
                                min={new Date().toISOString().split('T')[0]}
                                {...field}
                            />
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
                    <button
                        type="submit"
                        className="btn btn-primary w-24"
                        disabled={!isFormValid || createMutation.isPending}
                    >
                        {createMutation.isPending ? "Saving..." : "Save"}
                    </button>
                    <button
                        type="button"
                        className="btn btn-outline w-24"
                        onClick={handleCancel}
                    >
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
