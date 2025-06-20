import { create } from "zustand";
import { SortDirection, UserSortOption } from "@/types/enums";

interface SelectedUserInfo {
  id: number;
  firstName: string;
  lastName: string;
}

interface SelectUserModalState {
  page: number;
  search: string | null;
  sortBy: UserSortOption | null;
  sortDirection: SortDirection | null;
  selectedUser: SelectedUserInfo | null;
  setPage: (page: number) => void;
  setSearch: (search: string | null) => void;
  setSortBy: (sortBy: UserSortOption | null) => void;
  setSortDirection: (sortDirection: SortDirection | null) => void;
  setSelectedUser: (user: SelectedUserInfo | null) => void;
  reset: () => void;
}

export const useSelectUserModalStore = create<SelectUserModalState>((set) => ({
  page: 1,
  search: null,
  sortBy: null,
  sortDirection: null,
  selectedUser: null,
  setPage: (page) => set({ page }),
  setSearch: (search) => set({ search, page: 1 }),
  setSortBy: (sortBy) => set({ sortBy, page: 1 }),
  setSortDirection: (sortDirection) => set({ sortDirection, page: 1 }),
  setSelectedUser: (user) => set({ selectedUser: user }),
  reset: () => set({
    page: 1,
    search: null,
    sortBy: null,
    sortDirection: null,
    selectedUser: null,
  }),
}));