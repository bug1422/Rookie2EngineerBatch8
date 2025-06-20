import { ReturnRequestSortOption } from "@/types/enums";
import { useQuery } from "@tanstack/react-query";
import { returnRequestService } from "@/api/returnRequestService";
import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { SortDirection } from "@/types/enums";
import { useRequestForReturningListQueryStore } from "@/stores/requestForReturningListQueryStore";

const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

export const useReturnRequestData = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const {requestState, return_date, search, sort_by, sort_direction} = useRequestForReturningListQueryStore();
    
    const currentPage = parseInt(searchParams.get("page") || "1");
    const sortBy = (searchParams.get("sort_by") || sort_by || ReturnRequestSortOption.ID) as ReturnRequestSortOption;
    const sortDirection = (searchParams.get("sort_direction") || sort_direction || SortDirection.ASC) as SortDirection;
    
    useEffect(() => {
        if (isNaN(currentPage) || currentPage < 1) {
            updateUrlParams({ page: 1 });
        }
    }, [currentPage]);

    const { data: reportService, isLoading} = useQuery({
        queryKey: ["request", currentPage, sortBy, sortDirection, requestState, return_date, search],
        queryFn: () => returnRequestService.get_return_request_list(currentPage, PAGE_SIZE, sortBy, sortDirection, requestState, return_date ? return_date : undefined, search || undefined),
    })

    const requests = reportService?.data.data || [];
    const paginationMeta = reportService?.data.meta;

    useEffect(() => {
        if (paginationMeta && currentPage > paginationMeta.total_pages && paginationMeta.total_pages > 0) {
            updateUrlParams({ page: paginationMeta.total_pages });
        }
    }, [paginationMeta, currentPage]);

    useEffect(() => {
        updateUrlParams({ page: 1 });
    }, [requestState, return_date, search, sort_by, sort_direction]);
    
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
    }

    const handleSort = (newSortBy: ReturnRequestSortOption) => {
        let newSortDirection: SortDirection;
        
        if (sortBy === newSortBy) {
            newSortDirection = sortDirection === SortDirection.ASC ? SortDirection.DESC : SortDirection.ASC;
        } else {
            newSortDirection = SortDirection.DESC;
        }

        updateUrlParams({
            sort_by: newSortBy,
            sort_direction: newSortDirection
        });
    };

    const handlePageChange = (newPage: number) => {
        updateUrlParams({ page: newPage });
    };

    return {
        requests,
        isLoading,
        paginationMeta,
        currentPage,
        sortBy,
        sortDirection,
        handleSort,
        handlePageChange,
    }
}
