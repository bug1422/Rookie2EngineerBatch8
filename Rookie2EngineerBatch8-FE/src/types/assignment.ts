import { AssetDetail } from "./asset";
import {
  AssignmentSortOption,
  AssignmentState,
  MyAssignmentSortOption,
  SortDirection,
} from "./enums";
import { UserDetail } from "./user";

export interface AssignmentListQueryParams {
  page: number;
  asset_id?: number;
  assignmentState?: AssignmentState;
  assigned_date?: string;
  search?: string;
  sortBy?: AssignmentSortOption;
  sortDirection?: SortDirection;
}

export interface AssignmentDetail {
  id?: number;
  asset_id?: number;
  assigned_to_id?: string;
  assigned_by_id?: string;
  assigned_to_username?: string;
  assigned_by_username?: string;
  assign_date?: string;
  assignment_state?: AssignmentState;
  assignment_note?: string;
  asset?: AssetDetail;
}

export interface AssignmentListResponse {
  id: number;
  assign_date: string;
  assignment_state: AssignmentState;
}

export interface MyAssignmentDetail {
  id?: number;
  assign_date?: string;
  assignment_note?: string;
  assignment_state?: AssignmentState;
  assigned_to_user?: UserDetail;
  assigned_by_user?: UserDetail;
  asset?: AssetDetail;
}

export interface MyAssignmentListQueryParams {
  page: number;
  sortBy?: MyAssignmentSortOption;
  sortDirection?: SortDirection;
}


export interface AssignmentSimple {
  id: number;
  assigned_to: number;
  assigned_by: number;
  assign_date: string;
  assignment_state: AssignmentState;
  assignment_note?: string;
}

export interface AssignmentDetailNew {
  assignment: AssignmentSimple;
  asset: AssetDetail;
  assigned_to_user: UserDetail;
  assigned_by_user: UserDetail;
}

export interface AssignmentDetailUpdateForm {
  assigned_to_id: number;
  assigned_by_id: number;
  asset_id: number;
  assign_date: string;
  assignment_note?: string;
}

export interface AssignmentCreateForm {
  assigned_to_id: number;
  asset_id: number;
  assign_date: string;
  assignment_note?: string;
}
