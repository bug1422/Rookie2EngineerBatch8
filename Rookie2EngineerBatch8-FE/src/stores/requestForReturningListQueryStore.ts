import { RequestState, SortDirection, ReturnRequestSortOption } from "@/types/enums";
import { ReturnRequestListQueryParams } from "@/types/return_request";
import { create } from "zustand";

interface RequestForReturningListQueryState extends ReturnRequestListQueryParams {
  setPage: (page: number) => void;
  setRequestState: (requestState: RequestState | undefined) => void;
  setReturnDate: (returnDate: Date | null) => void;
  setSearch: (search: string | null) => void;
  setSortBy: (sortBy: ReturnRequestSortOption | undefined) => void;
  setSortDirection: (sortDirection: SortDirection | undefined) => void;
  reset: () => void;
}

const initialState: ReturnRequestListQueryParams = {
  page: 1,
  requestState: undefined,
  return_date: null,
  search: null,
  sort_by: ReturnRequestSortOption.ID,
  sort_direction: SortDirection.ASC,
};

export const useRequestForReturningListQueryStore = create<RequestForReturningListQueryState>((set) => ({
    ...initialState,

    setPage: (page) => set((state) => ({ ...state, page})),

    setRequestState: (requestState) => set((state) => ({ ...state, requestState})),

    setReturnDate: (return_date: Date | null) => set((state) => ({ ...state, return_date: return_date})),

    setSearch: (search) => set((state) => ({ ...state, search})),

    setSortBy: (sort_by) => set((state) => ({ ...state, sort_by})),

    setSortDirection: (sort_direction) => set((state) => ({ ...state, sort_direction})),

    reset: () => set(initialState),
}));