import { Modal } from "@/components/UI/Modal";
import Pagination from "@/components/UI/Pagination";
import { useDebounce } from "@/hooks/useDebounce";
import { useAssignmentListQueryStore } from "@/stores/assignmentListQueryStore";
import { AssignmentDetail } from "@/types/assignment";
import { AssignmentSortOption, SortDirection } from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import { HTMLAttributes, useState } from "react";
import SortOptions from "@/components/UI/SortOptions";
import { AssignmentPopUp } from "@/components/UI/PopUp/AssignmentPopUp";
import { AssignmentActionContent } from "./actionContent";
import { assignmentListQueryKey } from "./assignmentQuery";
import { ConfirmationModalPopUp } from "@/components/UI/Modal/ConfirmationModal";
import { useQueryClient } from "@tanstack/react-query";
import { assignmentService } from "@/api/assignmentService";
import { returnRequestService } from "@/api/returnRequestService";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";
import { AssignmentActionType } from "@/types/enums";

interface AssignmentTableProps extends Partial<HTMLAttributes<HTMLDivElement>> {
  assignmentsInfo?: PaginatedResponse<AssignmentDetail[]>;
  isLoading?: boolean;
  pageSize: number;
}

export default function AssignmentTable({
  assignmentsInfo,
  isLoading,
  pageSize,
  ...props
}: AssignmentTableProps) {
  const queryClient = useQueryClient();
  const assignments = assignmentsInfo?.data;
  const paginationMeta = assignmentsInfo?.meta;
  const isEmpty = assignments === undefined || assignments.length === 0;
  const { page, sortBy, sortDirection, setSortBy, setSortDirection, setPage } =
    useAssignmentListQueryStore();
  const [currentSortBy, setCurrentSortBy] = useState<AssignmentSortOption>(
    sortBy || AssignmentSortOption.ID
  );
  const [currentSortDirection, setCurrentSortDirection] =
    useState<SortDirection>(sortDirection || SortDirection.NONE);
  const [isModalOpen, setModalOpen] = useState(false);
  const [isConfirmationModalOpen, setConfirmationModalOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] =
    useState<AssignmentDetail | null>(null);
  const [confirmationText, setConfirmationText] = useState<string>();
  const [confirmationAction, setConfirmationAction] = useState<string>();

  const refetchAssignmentList = () => {
    queryClient.invalidateQueries({
      queryKey: [assignmentListQueryKey],
    });
  };

  const deleteAssignment = async (assignmentId: number) => {
    try {
      await assignmentService.delete_assignment(assignmentId);
      toast({
        content: `You have deleted assignment with id: ${assignmentId}`,
        alertType: "alert-success",
        duration: 3,
      });
      refetchAssignmentList();
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
      refetchAssignmentList();
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

  const debouncedSet = useDebounce(
    (key: AssignmentSortOption, direction: SortDirection) => {
      setSortBy(key);
      setSortDirection(direction);
    },
    300
  );
  const SORT_OPTIONS = [
    { key: AssignmentSortOption.ID, label: "No." },
    { key: AssignmentSortOption.ASSET_CODE, label: "Asset Code" },
    { key: AssignmentSortOption.ASSET_NAME, label: "Asset Name" },
    { key: AssignmentSortOption.ASSIGNED_TO, label: "Assigned To" },
    { key: AssignmentSortOption.ASSIGNED_BY, label: "Assigned By" },
    { key: AssignmentSortOption.ASSIGNED_DATE, label: "Assigned Date" },
    { key: AssignmentSortOption.STATE, label: "State" },
  ];
  const handleToggle = (
    key: AssignmentSortOption,
    direction: SortDirection
  ) => {
    setCurrentSortBy(key);
    setCurrentSortDirection(direction);
    debouncedSet(key, direction);
  };
  const handleSelectAssignment = (assignment: AssignmentDetail) => {
    setSelectedAssignment(assignment);
    setModalOpen(true);
  };

  const AssignmentDetailBody = ({
    assignment,
  }: {
    assignment: AssignmentDetail | null;
  }) => {
    if (assignment === null) return "No User Found";
    return (
      <AssignmentPopUp
        value={assignment}
        actionContent={AssignmentActionContent({
          assignment,
          setModalOpen: setModalOpen,
          setConfirmationText: setConfirmationText,
          setConfirmationAction: setConfirmationAction,
        })}
      />
    );
  };

  const renderEmptyRows = (pageSize: number) => {
    const filledRows = assignments?.length || 0;
    const emptyRowsCount = Math.max(0, pageSize - filledRows);

    if (emptyRowsCount <= 0) return null;

    return Array.from({ length: emptyRowsCount }).map((_, index) => (
      <tr key={`empty-${index}`} className="h-12">
        {Array.from({ length: SORT_OPTIONS.length }).map((_, colIndex) => (
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
        header={"Detailed Assignment Information"}
        body={<AssignmentDetailBody assignment={selectedAssignment} />}
      />

      <ConfirmationModalPopUp
        isOpen={isConfirmationModalOpen}
        setOpen={(open: boolean) => setConfirmationModalOpen(open)}
        confirmationText={confirmationText}
        onConfirm={() => {
          if (confirmationAction === AssignmentActionType.DELETE) {
            if (selectedAssignment) {
              deleteAssignment(selectedAssignment?.id ?? 0);
            }
          } else if (confirmationAction === AssignmentActionType.RETURN_REQUEST) {
            if (selectedAssignment) {
              requestReturnAssignment(selectedAssignment?.id ?? 0);
            }
          }
        }}
      />

      <div className="w-full mt-1 overflow-x-auto my-2 rounded-lg border border-base-300" {...props}>
        <table
          id="assignment-list-table"
          className="hidden md:table table-xs w-full border-collapse"
        >
          <colgroup>
            <col className="w-[5%]" />
            <col className="w-[10%]" />
            <col className="w-[15%]" />
            <col className="w-[15%]" />
            <col className="w-[15%]" />
            <col className="w-[15%]" />
            <col className="w-[15%]" />
            <col className="w-[10%]" />
          </colgroup>
          <thead>
            <tr id="assignment-sortbar" className="text-sm md:text-base bg-base-200/50 border-b border-base-300 h-12">
              {SORT_OPTIONS.map((option) => (
                <th className="text-sm !py-0" key={option.key}>
                  <SortOptions
                    key={option.key}
                    option={option}
                    currentSortBy={currentSortBy}
                    currentSortDirection={currentSortDirection}
                    onToggle={handleToggle}
                  />
                </th>
              ))}
            </tr>
          </thead>
          <tbody id="assignment-list-container" className="bg-base-100 divide-y divide-base-300">
            {isLoading ? (
              <>
                {Array.from({ length: pageSize }, (_, index) => index + 1).map(
                  (_, index) => (
                    <tr
                      id="user-list-loading"
                      key={index}
                      className="w-full text-sm md:text-base"
                    >
                      {Array.from({ length: pageSize }, (_, index) => index + 1).map(
                        (_, index) => (
                          <td
                            key={index}
                            className="whitespace-nowrap px-2 py-3"
                          >
                            <div className="w-2/3 h-6 skeleton"></div>
                          </td>
                        )
                      )}
                    </tr>
                  )
                )}
              </>
            ) : isEmpty ? (
              <tr className="h-[20rem] w-full">
                <td colSpan={8} className="text-center align-center">
                  <span className="text-primary font-bold text-5xl">
                    No Assignments Found!
                  </span>
                </td>
              </tr>
            ) : (
              <>
                {assignments?.map((assignment, index) => (
                  <tr
                    id={`assignment-list-item-${assignment.id}`}
                    key={index}
                    className="hover:bg-base-200 transition-colors cursor-pointer text-sm"
                    onClick={() => handleSelectAssignment(assignment)}
                  >
                    <td className="px-2 py-3">{assignment.id}</td>
                    <td
                      className="px-2 py-3"
                      title={assignment.asset?.asset_code}
                    >
                      {assignment.asset?.asset_code}
                    </td>
                    <td
                      className="px-2 py-3 truncate"
                      title={assignment.asset?.asset_name}
                    >
                      {assignment.asset?.asset_name}
                    </td>
                    <td className="px-2 py-3 truncate">
                      {assignment.assigned_to_username}
                    </td>
                    <td className="px-2 py-3 truncate">
                      {assignment.assigned_by_username}
                    </td>
                    <td className="px-2 py-3">
                      {assignment.assign_date
                        ? new Date(assignment.assign_date).toLocaleDateString(
                            "en-GB"
                          )
                        : "N/A"}
                    </td>
                    <td
                      className="px-2 py-3"
                      title={assignment.assignment_state}
                    >
                      <span>{assignment.assignment_state}</span>
                    </td>
                    <td
                      className="flex justify-start lg:gap-1 space-x-0.5 px-2 py-3"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <AssignmentActionContent
                        assignment={assignment}
                        setModalOpen={setConfirmationModalOpen}
                        setConfirmationText={setConfirmationText}
                        setConfirmationAction={setConfirmationAction}
                        setSelectedAssignment={setSelectedAssignment}
                        requestReturnAssignment={requestReturnAssignment}
                      />
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
              className="w-full my-3 justify-around flex flex-row gap-4"
            >
              <div className="flex gap-2">
                <select 
                  className="select select-bordered w-3/4"
                  onChange={(e) => {
                    const selectedOption = SORT_OPTIONS.find(
                      option => option.key === e.target.value
                    );
                    if (selectedOption) {
                      handleToggle(selectedOption.key as AssignmentSortOption, SortDirection.ASC);
                    }
                  }}
                >
                  <option value="">Sort by...</option>
                  {SORT_OPTIONS.map((option) => (
                    <option key={option.key} value={option.key}>
                      {option.label}
                    </option>
                  ))}
                </select>
                <button 
                  className="btn btn-outline w-1/4"
                  onClick={() => {
                    if (currentSortBy) {
                      handleToggle(
                        currentSortBy,
                        currentSortDirection === SortDirection.ASC 
                          ? SortDirection.DESC 
                          : SortDirection.ASC
                      );
                    }
                  }}
                >
                  {currentSortDirection === SortDirection.ASC ? '↑' : '↓'}
                </button>
              </div>
              {/* {SORT_OPTIONS.map((option) => (
                <SortOptions
                  key={option.key}
                  option={option}
                  currentSortBy={currentSortBy}
                  currentSortDirection={currentSortDirection}
                  onToggle={handleToggle}
                  className="text-sm"
                  toggleClassName="w-full"
                />
              ))} */}
            </div>
            {isLoading ? (
              <>
                {Array.from({ length: 7 }, (_, index) => index + 1).map(
                  (_, index) => (
                    <div
                      key={index}
                      className="w-full p-4 space-y-2 hover:bg-base-200"
                    >
                      {SORT_OPTIONS.map((option, idx) => (
                        <div
                          key={idx}
                          className="flex justify-between items-center"
                        >
                          <span className="font-bold text-sm text-neutral/70">
                            {option.label}
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
                {assignments?.map((assignment, index) => (
                  <div
                    key={index}
                    className="w-full p-4 space-y-2 hover:bg-base-200 transition-colors cursor-pointer active:bg-base-300"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSelectAssignment(assignment);
                    }}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        No.
                      </span>
                      <span className="text-sm">{assignment.id}</span>
                    </div>
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
                        Assigned To
                      </span>
                      <span className="text-sm">
                        {assignment.assigned_to_username}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Assigned By
                      </span>
                      <span className="text-sm">
                        {assignment.assigned_by_username}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        Assigned Date
                      </span>
                      <span className="text-sm">{assignment.assign_date}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-neutral/70">
                        State
                      </span>
                      <span className="text-sm">
                        {assignment.assignment_state}
                      </span>
                    </div>
                  </div>
                ))}
              </>
            )}
          </div>
        </div>
      </div>
      <div className="pt-4">
        {paginationMeta && (
          <Pagination
            isLoading={paginationMeta == undefined}
            currentPage={page}
            maxPage={paginationMeta.total_pages}
            onChange={(value: number) => setPage(value)}
          />
        )}
      </div>
    </>
  );
}
