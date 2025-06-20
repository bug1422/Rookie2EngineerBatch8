import { AssignmentDetail, MyAssignmentDetail } from "@/types/assignment";
import { ReactNode } from "react";
// import { Link } from "react-router-dom";

interface MyAssignmentPopUpProps {
    value: MyAssignmentDetail;
    actionContent?: string | ReactNode;
}

interface AssignmentPopUpProps {
    value: AssignmentDetail;
    actionContent?: string | ReactNode;
}

export function MyAssignmentPopUp({ value, actionContent }: MyAssignmentPopUpProps) {

    return (
      <div className="relative grid grid-cols-3 gap-y-2 text-neutral/60 text-sm">
        <div className="col-span-1">Asset Code</div>
        <div className="col-span-2">{value.asset?.asset_code}</div>
        <div className="col-span-1">Asset Name</div>
        <div className="col-span-2">{value.asset?.asset_name}</div>
        <div className="col-span-1">Specification</div>
        <div className="col-span-2">{value.asset?.specification}</div>
        <div className="col-span-1">Assigned To</div>
        <div className="col-span-2">{value.assigned_to_user?.username}</div>
        <div className="col-span-1">Assigned By</div>
        <div className="col-span-2">{value.assigned_by_user?.username}</div>
        <div className="col-span-1">Assigned Date</div>
        <div className="col-span-2">
          {value?.assign_date ? new Date(value.assign_date).toLocaleDateString("en-GB") : "N/A"}
        </div>
        <div className="col-span-1">State</div>
        <div className="col-span-2">{value?.assignment_state}</div>
        <div className="col-span-1">Note</div>
        <div className="col-span-2">
          {value.assignment_note ? (
            <span className="text-sm">{value.assignment_note}</span>
          ) : (
            <span className="text-sm text-neutral/50">No Note</span>
          )}
        </div>
        <div className="md:hidden">{actionContent}</div>
        
      </div>
    );
}

export function AssignmentPopUp({ value, actionContent }: AssignmentPopUpProps) {

    return (
      <div className="relative grid grid-cols-3 gap-y-2 text-neutral/60 text-sm">
        <div className="col-span-1">Asset Code</div>
        <div className="col-span-2">{value.asset?.asset_code}</div>
        <div className="col-span-1">Asset Name</div>
        <div className="col-span-2">{value.asset?.asset_name}</div>
        <div className="col-span-1">Specification</div>
        <div className="col-span-2">{value.asset?.specification}</div>
        <div className="col-span-1">Assigned To</div>
        <div className="col-span-2">{value.assigned_to_username}</div>
        <div className="col-span-1">Assigned By</div>
        <div className="col-span-2">{value.assigned_by_username}</div>
        <div className="col-span-1">Assigned Date</div>
        <div className="col-span-2">
          {value.assign_date ? new Date(value.assign_date).toLocaleDateString("en-GB") : "N/A"}
        </div>
        <div className="col-span-1">State</div>
        <div className="col-span-2">{value.assignment_state}</div>
        <div className="col-span-1">Note</div>
        <div className="col-span-2">
          {value.assignment_note ? (
            <span className="text-sm">{value.assignment_note}</span>
          ) : (
            <span className="text-sm text-neutral/50">No Note</span>
          )}
        </div>
        <div className="md:hidden">{actionContent}</div>
        
      </div>
    );
}