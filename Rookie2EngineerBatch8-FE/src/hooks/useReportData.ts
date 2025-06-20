import { useQuery } from "@tanstack/react-query";
import { reportService } from "@/api/reportService";
import { ReportSortOption, SortDirection } from "@/types/enums";
import { useSearchParams } from "react-router-dom";
import { useEffect } from "react";

const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

interface UseReportDataProps {
    defaultSortBy?: ReportSortOption;
    defaultSortDirection?: SortDirection;
}

export const useReportData = ({
    defaultSortBy = ReportSortOption.CATEGORY,
    defaultSortDirection = SortDirection.ASC,
}: UseReportDataProps = {}) => {
    const [searchParams, setSearchParams] = useSearchParams();

    const currentPage = parseInt(searchParams.get("page") || "1");
    const sortBy = (searchParams.get("sort_by") || defaultSortBy) as ReportSortOption;
    const sortDirection = (searchParams.get("sort_direction") || defaultSortDirection) as SortDirection;

    useEffect(() => {
        if (isNaN(currentPage) || currentPage < 1) {
            updateUrlParams({ page: 1 });
        }
    }, [currentPage]);

    const { data: reportResponse, isLoading } = useQuery({
        queryKey: ["report", currentPage, sortBy, sortDirection],
        queryFn: () => reportService.get_report_list(currentPage, PAGE_SIZE, sortBy, sortDirection),
    });

    const reports = reportResponse?.data.data || [];
    const paginationMeta = reportResponse?.data.meta;

    useEffect(() => {
        if (paginationMeta && currentPage > paginationMeta.total_pages && paginationMeta.total_pages > 0) {
            updateUrlParams({ page: paginationMeta.total_pages });
        }
    }, [paginationMeta, currentPage]);

    const updateUrlParams = (updates: Record<string, string | number>) => {
        setSearchParams(
            (params) => {
                Object.entries(updates).forEach(([key, value]) => {
                    params.set(key, value.toString().toLowerCase());
                });
                return params;
            },
            { replace: true }
        );
    };

    const handleSort = (newSortBy: ReportSortOption) => {
        let newSortDirection: SortDirection;

        if (sortBy === newSortBy) {
            newSortDirection = sortDirection === SortDirection.ASC ? SortDirection.DESC : SortDirection.ASC;
        } else {
            newSortDirection = SortDirection.DESC;
        }

        updateUrlParams({
            page: 1,
            sort_by: newSortBy,
            sort_direction: newSortDirection,
        });
    };

    const handlePageChange = (newPage: number) => {
        updateUrlParams({ page: newPage });
    };

    return {
        reports,
        isLoading,
        paginationMeta,
        currentPage,
        sortBy,
        sortDirection,
        handleSort,
        handlePageChange,
    };
};
