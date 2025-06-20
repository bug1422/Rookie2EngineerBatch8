import { AssignmentSortOption, AssignmentState, MyAssignmentSortOption, SortDirection } from "@/types/enums";
import { AssignmentListQueryParams, MyAssignmentListQueryParams } from "@/types/assignment";
import { create } from "zustand";

interface AssignmentListQueryState extends AssignmentListQueryParams {
  setPage: (page: number) => void;
  setAssetId: (asset_id: number | undefined) => void;
  setAssignemtnSate: (assignmentState: AssignmentState | undefined) => void;
  setAssignedDate: (assigned_date: string | undefined) => void;
  setSearch: (search: string | undefined) => void;
  setSortBy: (sortBy: AssignmentSortOption | undefined) => void;
  setSortDirection: (sortDirection: SortDirection | undefined) => void;
  reset: () => void;
}
interface MyAssignmentListQueryState extends MyAssignmentListQueryParams {
  setPage: (page: number) => void;
  setSortBy: (sortBy: MyAssignmentSortOption | undefined) => void;
  setSortDirection: (sortDirection: SortDirection | undefined) => void;
  reset: () => void;
}
const initialState: AssignmentListQueryParams = {
  page: 1,
  asset_id: undefined,
  assignmentState: undefined,
  assigned_date: undefined,
  search: undefined,
  sortBy: undefined,
  sortDirection: undefined,
};

const myAssignmentInitialState: MyAssignmentListQueryParams = {
  page: 1,
  sortBy: undefined,
  sortDirection: undefined,
};
export const useAssignmentListQueryStore = create<AssignmentListQueryState>((set) => ({
  ...initialState,

    setPage: (page) => set((state) => ({ ...state, page })),

    setAssetId: (asset_id) => set((state) => ({ ...state, asset_id })),

    setAssignemtnSate: (assignmentState) => set((state) => ({ ...state, assignmentState })),

    setAssignedDate: (assigned_date) => set((state) => ({ ...state, assigned_date })),

    setSearch: (search) => set((state) => ({ ...state, search })),

    setSortBy: (sortBy) => set((state) => ({ ...state, sortBy })),

    setSortDirection: (sortDirection) => set((state) => ({ ...state, sortDirection })),

  reset: () => set(initialState),
}));

export const useMyAssignemtnListQueryStore = create<MyAssignmentListQueryState>((set) => ({
  ...myAssignmentInitialState,
  
    setPage: (page) => set((state) => ({ ...state, page })),

    setSortBy: (sortBy) => set((state) => ({ ...state, sortBy })),

    setSortDirection: (sortDirection) => set((state) => ({ ...state, sortDirection })),

  reset: () => set(myAssignmentInitialState),
}));
