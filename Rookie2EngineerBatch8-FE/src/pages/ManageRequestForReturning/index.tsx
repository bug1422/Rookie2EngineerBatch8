import PageLayout from "@/components/layouts/PageLayout";
import { ReturnRequestTable } from "./table";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import Pagination from "@/components/UI/Pagination";
import { useReturnRequestData } from "@/hooks/useReturnRequestData";
import { ConfirmationModal } from "@/components/UI/Modal";
import { useState } from "react";
import { ReturnRequestResponse } from "@/types/return_request";
import { returnRequestService } from "@/api/returnRequestService";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";
import { RequestForReturningToolbar } from "./toolbar";

export default function RequestForReturning() {
    useBreadcrumbs([{ label: "Request for Returning" }]);

    const { requests, isLoading, paginationMeta, currentPage, sortBy, sortDirection, handleSort, handlePageChange } = useReturnRequestData();

    // State for confirmation modals
    const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
    const [isCompleteModalOpen, setIsCompleteModalOpen] = useState(false);
    const [selectedRequest, setSelectedRequest] = useState<ReturnRequestResponse | null>(null);

    const queryClient = useQueryClient();

    // Cancel request mutation
    const cancelMutation = useMutation({
        mutationFn: (requestId: number) => returnRequestService.cancel_request(requestId),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["request"],
                exact: false
            });
            toast({
                content: "Return request has been cancelled successfully",
                alertType: "alert-success",
                duration: 3,
            });
            setIsCancelModalOpen(false);
            setSelectedRequest(null);
        },
        onError: (error: AxiosError<{ detail: string }>) => {
            const errorMessage = error.response?.data?.detail || "Failed to cancel return request";
            toast({
                content: errorMessage,
                alertType: "alert-error",
                duration: 3,
            });
            setIsCancelModalOpen(false);
            setSelectedRequest(null);
        },
    });

    // use Mutation for completing a return request (for consistency with cancel)
    const completeMutation = useMutation({
        mutationFn: (requestId: number) => returnRequestService.complete_request(requestId),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["request"],
                exact: false
            });
            toast({
                content: "Return request has been completed successfully",
                alertType: "alert-success",
                duration: 3,
            });
            setIsCompleteModalOpen(false);
            setSelectedRequest(null);
        },
        onError: (error: AxiosError<{ detail: string }>) => {
            const errorMessage = error.response?.data?.detail || "Failed to complete return request";
            toast({
                content: errorMessage,
                alertType: "alert-error",
                duration: 3,
            });
            setIsCompleteModalOpen(false);
            setSelectedRequest(null);
        },
    });

    const handleCancelRequest = (request: ReturnRequestResponse) => {
        setSelectedRequest(request);
        setIsCancelModalOpen(true);
    };

    const handleCompleteRequest = (request: ReturnRequestResponse) => {
        setSelectedRequest(request);
        setIsCompleteModalOpen(true);
    };

    const handleConfirmCancel = () => {
        if (selectedRequest) {
            cancelMutation.mutate(selectedRequest.id);
        }
    };

    const handleConfirmComplete = () => {
        if (selectedRequest) {
            completeMutation.mutate(selectedRequest.id);
        }
    };

    const handleCloseCancelModal = () => {
        setIsCancelModalOpen(false);
        setSelectedRequest(null);
    };

    const handleCloseCompleteModal = () => {
        setIsCompleteModalOpen(false);
        setSelectedRequest(null);
    };

    return (
        <PageLayout title="Request for Returning">
            <RequestForReturningToolbar />
            <ReturnRequestTable
                requests={requests}
                isLoading={isLoading}
                pageSize={20}
                sortBy={sortBy}
                sortDirection={sortDirection}
                onSort={handleSort}
                onApprove={handleCompleteRequest}
                onCancel={handleCancelRequest}
            />

            <div className="flex justify-end items-center w-full">
                <Pagination
                    isLoading={isLoading}
                    currentPage={currentPage}
                    maxPage={paginationMeta?.total_pages || 0}
                    onChange={handlePageChange}
                />
            </div>

            {/* Cancel Confirmation Modal */}
            <ConfirmationModal
                isOpen={isCancelModalOpen}
                onClose={handleCloseCancelModal}
                header="Are you sure?"
                body="Do you want to cancel this returning request?"
                callback={handleConfirmCancel}
                confirmText="Yes"
                cancelText="No"
                useCloseButton={false}
            />

            {/* Complete Confirmation Modal */}
            <ConfirmationModal
                isOpen={isCompleteModalOpen}
                onClose={handleCloseCompleteModal}
                header="Are you sure?"
                body={
                    selectedRequest 
                        ? `Do you want to mark this returning request for asset "${selectedRequest.asset.asset_name}" as 'Completed'?`
                        : "Do you want to mark this returning request as 'Completed'?"
                }
                callback={handleConfirmComplete}
                confirmText="Yes"
                cancelText="No"
                useCloseButton={false}
            />
        </PageLayout>
    )
}