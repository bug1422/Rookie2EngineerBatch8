import { RequestState, ReturnRequestSortOption } from "@/types/enums";
import axiosClient from "./axiosClient";
import { PaginatedResponse } from "@/types/meta";
import { SortDirection } from "@/types/enums";
import { ReturnRequestResponse } from "@/types/return_request";
import { RequestCreate } from "@/types/return_request";


const API_BASE_ROUTE = `/v1/requests`;
const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

export const returnRequestService = {
    get_return_request_list: (page: number, size?: number, sortBy?: ReturnRequestSortOption, sortDirection?: SortDirection, state?: RequestState, return_date?: Date, search?: string) => {
        return axiosClient.get<PaginatedResponse<ReturnRequestResponse[]>>(API_BASE_ROUTE, {
            params: {
                page,
                size: size || PAGE_SIZE,
                sort_by: sortBy,
                sort_direction: sortDirection,
                state,
                return_date: return_date?.toISOString(),
                search
            }
        });
    },
    create_request: (data: RequestCreate) => {
        return axiosClient.post<ReturnRequestResponse>(API_BASE_ROUTE, data);
    },

    cancel_request: (requestId: number) => {
        return axiosClient.delete(`${API_BASE_ROUTE}/${requestId}`);
    },

    complete_request: (requestId: number) => {
        return axiosClient.patch(`${API_BASE_ROUTE}/${requestId}`, {
            request_state: "Completed"
        });
    },

};