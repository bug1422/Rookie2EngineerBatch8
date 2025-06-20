import Pagination from "@/components/UI/Pagination";
import { useDebounce } from "@/hooks/useDebounce";
import {
  AssignmentState,
  MyAssignmentSortOption,
  SortDirection,
} from "@/types/enums";
import { PaginatedResponse, PaginationMeta } from "@/types/meta";
import { Check, RotateCcw, X } from "lucide-react";
import { HTMLAttributes, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { AssignmentDetail, MyAssignmentDetail } from "@/types/assignment";
import { useMyAssignemtnListQueryStore } from "@/stores/assignmentListQueryStore";
import { Modal } from "@/components/UI/Modal";
import { MyAssignmentPopUp } from "@/components/UI/PopUp/AssignmentPopUp";
import SortOptions from "@/components/UI/SortOptions";
import { ConfirmationModalPopUp } from "@/components/UI/Modal/ConfirmationModal";
import { myAssgnmentListQueryKey } from "./myAssignmentQuery";
import { assignmentService } from "@/api/assignmentService";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";
import { returnRequestService } from "@/api/returnRequestService";
import { AssignmentActionType } from "@/types/enums";
interface MyAssignmentTableProps
  extends Partial<HTMLAttributes<HTMLDivElement>> {
  myAssignmentInfo: PaginatedResponse<MyAssignmentDetail[]> | undefined;
  paginationMeta: PaginationMeta | undefined;
  isLoading?: boolean;
  pageSize: number;
}

export default function MyAssignmentTable({
  myAssignmentInfo,
  paginationMeta,
  isLoading = false,
  pageSize,
  ...props
}: MyAssignmentTableProps) {
  const queryClient = useQueryClient();
  const myAssignment = myAssignmentInfo?.data;
  const isEmpty = myAssignment === undefined || myAssignment.length == 0;
  const { page, sortBy, sortDirection, setSortBy, setSortDirection, setPage } =
    useMyAssignemtnListQueryStore();
  const [currentSortBy, setCurrentSortBy] = useState<MyAssignmentSortOption>(
    sortBy ?? MyAssignmentSortOption.ASSET_CODE
  );
  const [currentSortDirection, setCurrentSortDirection] =
    useState<SortDirection>(sortDirection ?? SortDirection.NONE);
  const [isModalOpen, setModalOpen] = useState(false);
  const [isRequestModalOpen, setRequestModalOpen] = useState(false);
  const [confirmationText, setConfirmationText] = useState<string>();
  const [confirmationAction, setConfirmationAction] = useState<string>();
  const [selectedAssignment, setSelectedAssignment] =
    useState<MyAssignmentDetail | null>(null);

  const refetchMyAssignmentList = () => {
    queryClient.invalidateQueries({
      queryKey: [myAssgnmentListQueryKey],
    });
  };

  const responseToAssignment = async (
    selectedAssignment: MyAssignmentDetail | null,
    assignmentState: AssignmentState
  ) => {
    try {
      await assignmentService.response_to_assignment(
        selectedAssignment?.id ?? 0,
        assignmentState
      );
      toast({
        content: `You have successfully ${confirmationAction} with asset ${selectedAssignment?.asset?.asset_code}`,
        alertType: "alert-success",
        duration: 3,
      });
      refetchMyAssignmentList();
    } catch (error) {
      const axiosError = error as AxiosError<{ detail: string }>;
      const errorMessage =
        axiosError.response?.data?.detail || "Failed to update assignment";
      toast({
        content: errorMessage,
        alertType: "alert-error",
        duration: 3,
      });
    }
  };

  const requestReturnAssignment = async (assignmentId: number) => {
    try {
      if (!assignmentId) {
        throw new Error("Invalid assignment ID");
      }
      await returnRequestService.create_request({ assignment_id: assignmentId });
      toast({
        content: `Return request has been created for assignment with id: ${assignmentId}`,
        alertType: "alert-success",
        duration: 3,
      });
      refetchMyAssignmentList();
    } catch (error) {
      const axiosError = error as AxiosError<{ detail: string }>;
      const errorMessage =
        axiosError.response?.data?.detail || 
        axiosError.message || 
        "Failed to create return request";
      console.error("Return request error:", error);
      toast({
        content: errorMessage,
        alertType: "alert-error",
        duration: 3,
      });
    }
  };

  const SORT_OPTIONS = [
    { key: MyAssignmentSortOption.ASSET_CODE, label: "Asset Code" },
    { key: MyAssignmentSortOption.ASSET_NAME, label: "Asset Name" },
    { key: MyAssignmentSortOption.CATEGORY, label: "Category" },
    { key: MyAssignmentSortOption.ASSIGNED_DATE, label: "Assigned Date" },
    { key: MyAssignmentSortOption.STATE, label: "State" },
  ];

  const TITLE_OPTIONS = [
    "Asset Code",
    "Asset Name",
    "Category",
    "Assigned Date",
    "State",
  ];

  const debouncedSet = useDebounce(
    (key: MyAssignmentSortOption, direction: SortDirection) => {
      setSortBy(key);
      setSortDirection(direction);
    },
    300
  );
  const handleToggle = (
    key: MyAssignmentSortOption,
    direction: SortDirection
  ) => {
    setCurrentSortBy(key);
    setCurrentSortDirection(direction);
    debouncedSet(key, direction);
  };
  const handleSelectAssignment = (assignment: MyAssignmentDetail) => {
    setSelectedAssignment(assignment);
    setModalOpen(true);
  };

  // Action content for each assignment based on its state
  // This function returns the action buttons based on the assignment state
  const ActionContent = (assignment: MyAssignmentDetail) => {
    return (
      <>
        {assignment?.assignment_state ===
        AssignmentState.WAITING_FOR_ACCEPTANCE ? (
          <div>
            <div
              className="btn btn-ghost btn-sm btn-square"
              onClick={() => {
                setRequestModalOpen(true);
                setConfirmationText("accept");
                setConfirmationAction(AssignmentActionType.ACCEPT);
                setSelectedAssignment(assignment);
              }}
            >
              <Check className="cursor-pointer w-4 h-4" color="red" />
            </div>
            <div
              className="btn btn-ghost btn-sm btn-square"
              onClick={() => {
                setRequestModalOpen(true);
                setConfirmationText("decline");
                setConfirmationAction(AssignmentActionType.DECLINE);
                setSelectedAssignment(assignment);
              }}
            >
              <X className="cursor-pointer w-4 h-4" />
            </div>
            <div className="btn btn-ghost btn-sm btn-square">
              <RotateCcw color="gray" className="cursor-pointer w-4 h-4" />
            </div>
          </div>
        ) : (
          <div>
            <div className="btn btn-ghost btn-sm btn-square">
              <Check className="w-4 h-4 opacity-40" color="red" />
            </div>
            <div className="btn btn-ghost btn-sm btn-square">
              <X className="w-4 h-4 opacity-40" />
            </div>
            <div
              className="btn btn-ghost btn-sm btn-square"
              onClick={() => {
                setRequestModalOpen(true);
                setConfirmationAction(AssignmentActionType.RETURN_REQUEST);
                setConfirmationText("create a returning request for");
                setSelectedAssignment(assignment);
              }}
            >
              <RotateCcw color="blue" className="cursor-pointer w-4 h-4" />
            </div>
          </div>
        )}
      </>
    );
  };

  const MyAssignmentDetailBody = ({
    myAssignment,
  }: {
    myAssignment: AssignmentDetail | null;
  }) => {
    if (myAssignment === null) return "No User Found";
    return (
      <MyAssignmentPopUp
        value={myAssignment}
        actionContent={ActionContent(myAssignment)}
      />
    );
  };

  const renderEmptyRows = (totalRows: number) => {
    const filledRows = myAssignment?.length || 0;
    const emptyRowsCount = Math.max(0, totalRows - filledRows);

    if (emptyRowsCount <= 0) return null;

    return Array.from({ length: emptyRowsCount }).map((_, index) => (
      <tr key={`empty-${index}`} className="h-12">
        {Array.from({ length: SORT_OPTIONS.length + 1 }).map((_, colIndex) => (
          <td 
            key={`empty-cell-${colIndex}`} 
            className="bg-transparent border-0 px-2 py-3"
          />
        ))}
      </tr>
    ));
  };

  return (
    <>
      <Modal
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        header={"Detailed User Information"}
        body={<MyAssignmentDetailBody myAssignment={selectedAssignment} />}
      />
      <ConfirmationModalPopUp
        isOpen={isRequestModalOpen}
        setOpen={(open: boolean) => setRequestModalOpen(open)}
        confirmationText={confirmationText}
        onConfirm={() => {
          if (confirmationAction === AssignmentActionType.ACCEPT) {
            responseToAssignment(selectedAssignment, AssignmentState.ACCEPTED);
          } else if (confirmationAction === AssignmentActionType.DECLINE) {
            responseToAssignment(selectedAssignment, AssignmentState.DECLINED);
          } else if (confirmationAction === AssignmentActionType.RETURN_REQUEST) {
            const id = selectedAssignment?.id;
            if (id != null) {
              requestReturnAssignment(id);
            }
          }
        }}
      />
      <div className="w-full mt-1 overflow-x-auto my-2 rounded-lg border border-base-300" {...props}>
        <table className="hidden md:table table-xs w-full">
          <colgroup>
            <col className="w-1/9" />
            <col className="w-2/9" />
            <col className="w-1/9" />
            <col className="w-2/9" />
            <col className="w-1/9" />
            <col className="w-2/9" />
          </colgroup>
          <thead className="p-0">
            <tr className="text-sm md:text-base bg-base-200/50 border-b border-base-300 h-12">
              {SORT_OPTIONS.map((option) => (
                <th className="w-1/5 text-sm !py-0">
                  <SortOptions
                    key={option.key}
                    option={option}
                    currentSortBy={currentSortBy}
                    currentSortDirection={currentSortDirection}
                    onToggle={handleToggle}
                  />
                </th>
              ))}
              <th className="p-0"></th>
            </tr>
          </thead>
          <tbody id="my-assignment-list-container" className="w-full">
            {isLoading ? (
              <>
                {Array.from({ length: pageSize }, (_, index) => index + 1).map(
                  (_, index) => (
                    <tr
                      id="user-list-loading"
                      key={index}
                      className="w-full text-sm md:text-base"
                    >
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                    </tr>
                  )
                )}
              </>
            ) : isEmpty ? (
              <>
                <tr className="h-12">
                  <td colSpan={8} className="text-center text-base-content/60 px-4">
                      No data
                  </td>
                </tr>
                {renderEmptyRows(pageSize)}
              </>
            ) : (
              <>
                {myAssignment.map((assignment, index) => (
                  <tr
                    id={`assignment-list-item-${assignment?.id}`}
                    key={index}
                    className="hover:bg-base-200 transition-colors cursor-pointer text-sm md:text-base "
                    onClick={() => handleSelectAssignment(assignment)}
                  >
                    <td
                      title={assignment.asset?.asset_code}
                      className="whitespace-nowrap"
                    >
                      {assignment.asset?.asset_code}
                    </td>
                    <td
                      title={assignment.asset?.asset_name}
                      className="whitespace-nowrap truncate"
                    >
                      {assignment.asset?.asset_name}
                    </td>
                    <td
                      title={assignment.asset?.category.category_name}
                      className="whitespace-nowrap truncate"
                    >
                      {assignment.asset?.category.category_name}
                    </td>
                    <td
                      title={
                        assignment?.assign_date
                          ? new Date(assignment.assign_date).toLocaleDateString(
                              "en-GB"
                            )
                          : "N/A"
                      }
                      className="whitespace-nowrap"
                    >
                      {assignment?.assign_date
                        ? new Date(assignment.assign_date).toLocaleDateString(
                            "en-GB"
                          )
                        : "N/A"}
                    </td>
                    <td
                      title={assignment?.assignment_state}
                      className="whitespace-normal"
                    >
                      {assignment?.assignment_state}
                    </td>
                    <td
                      className="flex justify-start lg:gap-1 space-x-0.5 whitespace-nowrap"
                      onClick={(e) => e.stopPropagation()}
                    >
                      {ActionContent(assignment)}
                    </td>
                  </tr>
                ))}

                {renderEmptyRows(pageSize)}
              </>
            )}
          </tbody>
        </table>
        <div className="md:hidden">
          <div
            id="sm-assignment-list-container"
            className="flex flex-col divide-y-1 divide-neutral-content"
          >
            <div
              id="sm-assignment-sortbar"
              className="w-full my-3 justify-around flex flex-row"
            >
              {SORT_OPTIONS.map((option) => (
                <SortOptions
                  key={option.key}
                  option={option}
                  currentSortBy={currentSortBy}
                  currentSortDirection={currentSortDirection}
                  onToggle={handleToggle}
                  className="w-full"
                  toggleClassName="w-full"
                />
              ))}
            </div>
            {isLoading ? (
              <>
                {Array.from({ length: 5 }, (_, index) => index + 1).map(
                  (_, index) => (
                    <div
                      key={index}
                      className="w-full p-4 space-y-2 hover:bg-base-200"
                    >
                      {TITLE_OPTIONS.map((title) => (
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-sm text-neutral/70">
                            {title}
                          </span>
                          <div className="h-4 w-24 bg-gray-300 rounded animate-pulse"></div>
                        </div>
                      ))}
                    </div>
                  )
                )}
              </>
            ) : isEmpty ? (
              <div className="h-[20rem] w-full text-center align-center">
                <span className="text-primary font-bold text-5xl">
                  No Assignments Found!
                </span>
              </div>
            ) : (
              <>
                {myAssignment?.map((assignment, index) => (
                  <div
                    key={index}
                    className="w-full p-4 space-y-2 hover:bg-base-200 transition-colors cursor-pointer active:bg-base-300"
                    onClick={() => handleSelectAssignment(assignment)}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Asset Code
                      </span>
                      <span className="text-sm">
                        {assignment.asset?.asset_code}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Asset Name
                      </span>
                      <span className="text-sm">
                        {assignment.asset?.asset_name}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Category
                      </span>
                      <span className="text-sm">
                        {assignment.asset?.category.category_name}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Assigned Date
                      </span>
                      <span className="text-sm">
                        {assignment?.assign_date
                          ? new Date(assignment.assign_date).toLocaleDateString(
                              "en-GB"
                            )
                          : "N/A"}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        State
                      </span>
                      <span className="text-sm">
                        {assignment?.assignment_state}
                      </span>
                    </div>
                  </div>
                ))}
              </>
            )}
          </div>
        </div>
      </div>
      {paginationMeta && (
        <Pagination
          isLoading={paginationMeta == undefined}
          currentPage={page}
          maxPage={paginationMeta.total_pages}
          onChange={(value: number) => setPage(value)}
        />
      )}
    </>
  );
}
