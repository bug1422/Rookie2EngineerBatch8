import { SortDirection, Type, UserSortOption } from "@/types/enums";
import { UserListQueryParams } from "@/types/user";
import { create } from "zustand";

interface UserListQueryState extends UserListQueryParams {
  setPage: (page: number) => void;
  setType: (type: Type | undefined) => void;
  setSearch: (search: string | undefined) => void;
  setSortBy: (sortBy: UserSortOption | undefined) => void;
  setSortDirection: (sortDirection: SortDirection | undefined) => void;
  reset: () => void;
}
const initialState: UserListQueryParams = {
  page: 1,
  type: null,
  search: null,
  sortBy: null,
  sortDirection: null,
};
export const useUserListQueryStore = create<UserListQueryState>((set) => ({
  ...initialState,

  setPage: (page) => set((state) => ({ ...state, page })),

  setType: (type) => set((state) => ({ ...state, type, page: 1 })),

  setSearch: (search) => set((state) => ({ ...state, search, page: 1 })),

  setSortBy: (sortBy) => set((state) => ({ ...state, sortBy })),

  setSortDirection: (sortDirection) =>
    set((state) => ({ ...state, sortDirection })),

  reset: () => set(initialState),
}));
