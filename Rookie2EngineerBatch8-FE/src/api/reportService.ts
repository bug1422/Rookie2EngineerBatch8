import { SortDirection } from "@/types/enums";
import { ReportSortOption } from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import { Report } from "@/types/report";
import axiosClient from "@api/axiosClient";

const API_BASE_ROUTE = `/v1/reports`;
const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

export const reportService = {
    get_report_list: (page: number, size?: number, sortBy?: ReportSortOption, sortDirection?: SortDirection) => {
        return axiosClient.get<PaginatedResponse<Report[]>>(API_BASE_ROUTE, {
            params: { 
                page, 
                size: size || PAGE_SIZE, 
                sort_by: sortBy, 
                sort_direction: sortDirection 
            },
        });
    },
    download_report: () => {
        return axiosClient.get(`${API_BASE_ROUTE}/export`, {
            responseType: "blob"
        })
    }
};
