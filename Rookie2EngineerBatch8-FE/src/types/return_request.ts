import { RequestState, ReturnRequestSortOption, SortDirection } from "@/types/enums";
import { AssetDetail } from "@/types/asset";
import { UserReadSimple } from "@/types/user";

// Define a simple assignment type that matches the backend AssignmentReadSimple
export interface AssignmentSimple {
    id: number;
    assign_date: string;
    assignment_state: string;
    assignment_note?: string;
}

export interface ReturnRequestResponse {
    id: number;
    asset: AssetDetail;
    requested_by: UserReadSimple;
    accepted_by?: UserReadSimple | null;
    assignment: AssignmentSimple;  // Added the missing assignment field
    return_date?: Date | null;
    request_state: string;
}

export interface ReturnRequestListQueryParams {
    page?: number | 1;
    size?: number | 20;
    requestState?: RequestState;
    return_date?: Date | null;
    search?: string | null;
    sort_by?: ReturnRequestSortOption;
    sort_direction?: SortDirection;
}

export interface RequestCreate {
    assignment_id: number;
  }
