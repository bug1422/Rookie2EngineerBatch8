import { AssignmentDetail } from "@/types/assignment";
import { AssignmentState } from "@/types/enums";
import { CircleX, Pencil, RotateCcw } from "lucide-react";
import { Link } from "react-router-dom";
import { AssignmentActionType } from "@/types/enums";

interface ActionContentProps {
  assignment: AssignmentDetail;
  setModalOpen: (open: boolean) => void;
  setConfirmationText: (text: string) => void;
  setConfirmationAction: (action: string) => void;
  setSelectedAssignment?: (assignment: AssignmentDetail) => void;
  requestReturnAssignment?: (assignmentId: number) => Promise<void>;
}

export function AssignmentActionContent({
  assignment,
  setModalOpen,
  setConfirmationText,
  setConfirmationAction,
  setSelectedAssignment,
  
}: ActionContentProps) {
  // Action content for each assignment based on its state
  // This function returns the action buttons based on the assignment state// Action content for each assignment based on its state
  // This function returns the action buttons based on the assignment state
  return (
    <>
      {assignment.assignment_state ===
      AssignmentState.WAITING_FOR_ACCEPTANCE ? (
        <div className="flex justify-center gap-0.5">
          <Link
            to={`/manage-assignment/${assignment.id}`}
            className="btn btn-ghost btn-sm btn-square"
          >
            <Pencil className="w-4 h-4" stroke="white" fill="currentColor" />
          </Link>
          <div
            className="btn btn-ghost btn-sm btn-square"
            onClick={() => {
              setModalOpen(true);
              setConfirmationText("delete");
              setConfirmationAction(AssignmentActionType.DELETE);
              setSelectedAssignment?.(assignment);
            }}
          >
            <CircleX className="w-4 h-4" color="red" />
          </div>
          <div className="btn btn-ghost btn-sm btn-square opacity-40">
            <RotateCcw className="w-4 h-4" />
          </div>
        </div>
      ) : AssignmentState.DECLINED ? (
        <div className="flex justify-center gap-0.5">
          <div className="btn btn-ghost btn-sm btn-square">
            <Pencil
              className="w-4 h-4 opacity-40"
              stroke="white"
              fill="currentCollor"
            />
          </div>
          <div 
            className="btn btn-ghost btn-sm btn-square"
            onClick={() => {
              setModalOpen(true);
              setConfirmationText("delete");
              setConfirmationAction(AssignmentActionType.DELETE);
              setSelectedAssignment?.(assignment);
            }}  
          >
            <CircleX className="w-4 h-4" color="red" />
          </div>
          {assignment.assignment_state === AssignmentState.DECLINED ? (
            <div className="btn btn-ghost btn-sm btn-square opacity-40">
              <RotateCcw className="w-4 h-4" />
            </div>
          ) : (
            <div
              className="btn btn-ghost btn-sm btn-square"
              onClick={() => {
                setModalOpen(true);
                setConfirmationAction(AssignmentActionType.RETURN_REQUEST);
                setConfirmationText("create a returning request for");
                setSelectedAssignment?.(assignment);
              }}
            >
              <RotateCcw className="w-4 h-4" color="blue" />
            </div>
          )}
        </div>
      ) : (
        <div className="flex justify-center gap-0.5">
          <div className="btn btn-ghost btn-sm btn-square">
            <Pencil
              className="w-4 h-4 opacity-40"
              stroke="white"
              fill="currentCollor"
            />
          </div>
          <div className="btn btn-ghost btn-sm btn-square">
            <CircleX className="w-4 h-4 opacity-40" color="red" />
          </div>
          {assignment.assignment_state === AssignmentState.DECLINED ? (
            <div className="btn btn-ghost btn-sm btn-square opacity-40">
              <RotateCcw className="w-4 h-4" />
            </div>
          ) : (
            <div
              className="btn btn-ghost btn-sm btn-square"
              onClick={() => {
                setModalOpen(true);
                setConfirmationAction(AssignmentActionType.RETURN_REQUEST);
                setConfirmationText("create a returning request for");
                setSelectedAssignment?.(assignment);
              }}
            >
              <RotateCcw className="w-4 h-4" color="blue" />
            </div>
          )}
        </div>
      )}
    </>
  );
}
