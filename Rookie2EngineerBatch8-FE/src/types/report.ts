import { ReportSortOption, SortDirection } from "@/types/enums";

export interface Report {
    category: string;
    total: number;
    assigned: number;
    available: number;
    not_available: number;
    waiting_for_recycling: number;
    recycled: number;
}

export interface ReportListQueryParams {
    page?: number | 1;
    size?: number | 20;
    sort_by?: ReportSortOption;
    sort_direction?: SortDirection;
}
