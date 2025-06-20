import { AssignmentDetail, AssignmentDetailNew, AssignmentDetailUpdateForm, MyAssignmentDetail, AssignmentCreateForm } from "@/types/assignment";
import { AssetHistory } from "@/types/asset";
import {
  SortDirection,
  AssignmentSortOption,
  MyAssignmentSortOption,
  AssignmentState,
} from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import axiosClient from "@api/axiosClient";

const API_BASE_ROUTE = `/v1/assignments`;
const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;
export const assignmentService = {
  get_assignment_list: (
    page: number,
    size?: number,
    asset_id?: number,
    state?: AssignmentState,
    assign_date?: string,
    search?: string,
    sortBy?: AssignmentSortOption,
    sortDirection?: SortDirection
  ) => {
    return axiosClient.get<PaginatedResponse<AssignmentDetail[]>>(
      `${API_BASE_ROUTE}`,
      {
        params: {
          page: page,
          size: size || PAGE_SIZE,
          asset_id: asset_id,
          state: state,
          assign_date: 
            assign_date ? assign_date : null,
          search: search,
          sort_by: sortBy,
          sort_direction:
            sortDirection == SortDirection.NONE ? null : sortDirection,
        },
      }
    );
  },

  get_assign_home_list: (
    page: number,
    sortBy?: MyAssignmentSortOption,
    sortDirection?: SortDirection
  ) => {
    return axiosClient.get<PaginatedResponse<MyAssignmentDetail[]>>(
      `${API_BASE_ROUTE}/me`,
      {
        params: {
          page: page,
          size: PAGE_SIZE,
          sort_by: sortBy,
          sort_direction:
            sortDirection == SortDirection.NONE ? null : sortDirection,
        },
      }
    );
  },

  response_to_assignment: (
    assignment_id: number,
    assignment_state: AssignmentState
  ) => {
    return axiosClient.patch<AssignmentDetail>(
      `${API_BASE_ROUTE}/${assignment_id}`,
      {
        assignment_state: assignment_state,
      }
    );
  },

  delete_assignment: (assignment_id: number) => {
    return axiosClient.delete(`${API_BASE_ROUTE}/${assignment_id}`);
  },
  get_assignment_detail: (id: number) => {
    return axiosClient.get<AssignmentDetailNew>(`${API_BASE_ROUTE}/${id}`);
  },
  update_assignment: (id: number, data: AssignmentDetailUpdateForm) => {
    return axiosClient.put<AssignmentDetailUpdateForm>(`${API_BASE_ROUTE}/${id}`, data);
  },

  create_assignment: (data: AssignmentCreateForm) => {
    return axiosClient.post<AssignmentDetail>(`${API_BASE_ROUTE}`, data);
  },

  get_assignment_history: (
    page: number,
    asset_id: number
  ) => {
    return axiosClient.get<PaginatedResponse<AssetHistory[]>>(
      `${API_BASE_ROUTE}/history`,
      {
        params: {
          page: page,
          size: 5,
          asset_id: asset_id
        }
      }
    );
  }
};
