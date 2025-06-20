import { SortDirection, Type, UserSortOption } from "@/types/enums";
import { IsValid } from "@/types/isValid";
import { PaginatedResponse } from "@/types/meta";
import { UserBase, UserDetail, UserUpdate } from "@/types/user";
import axiosClient from "@api/axiosClient";

const API_BASE_ROUTE = `/v1/users`;
const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;
export const userService = {
  get_user_list: (
    page: number,
    type: Type | null,
    search: string | null,
    sortBy: UserSortOption | null,
    sortDirection: SortDirection | null,
    size?: number
  ) => {
    return axiosClient.get<PaginatedResponse<UserDetail[]>>(
      `${API_BASE_ROUTE}`,
      {
        params: {
          page: page,
          size: size || PAGE_SIZE,
          type: type,
          search: search,
          sort_by: sortBy,
          sort_direction:
            sortDirection == SortDirection.NONE ? null : sortDirection,
        },
      }
    );
  },
  get_user: (id: number) => {
    return axiosClient.get<UserDetail>(`${API_BASE_ROUTE}/${id}`);
  },
  update_user: (id: number, user: UserUpdate) => {
    return axiosClient.put<UserBase>(`${API_BASE_ROUTE}/${id}`, user);
  },
  delete_user: (id: number) => {
    return axiosClient.delete<UserBase>(`${API_BASE_ROUTE}/${id}`);
  },
  create_user: (user: UserBase) => {
    return axiosClient.post<UserBase>(`${API_BASE_ROUTE}`, user);
  },
  check_valid_user: (id: number) => {
    return axiosClient.get<IsValid>(`${API_BASE_ROUTE}/valid-user/${id}`);
  }
};
