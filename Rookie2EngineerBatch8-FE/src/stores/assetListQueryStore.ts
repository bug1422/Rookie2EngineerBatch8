import { SortDirection, AssetState, AssetSortOption } from "@/types/enums";
import { AssetListQueryParams } from "@/types/asset";
import { create } from "zustand";

interface AssetListQueryState extends AssetListQueryParams {
  setPage: (page: number) => void;
  setState: (state: AssetState[] | undefined) => void;
  setCategory: (category: string | undefined) => void;
  setSearch: (search: string | undefined) => void;
  setSortBy: (sortBy: AssetSortOption | undefined) => void;
  setSortDirection: (sortDirection: SortDirection | undefined) => void;
  reset: () => void;
}

const initialState: AssetListQueryParams = {
  page: 1,
  state: null,
  category: null,
  search: null,
  sortBy: null,
  sortDirection: null,
};

export const useAssetListQueryStore = create<AssetListQueryState>((set) => ({
  ...initialState,

  setPage: (page) => set((state) => ({ ...state, page })),

  setState: (newState) =>
    set((state) => ({ ...state, state: newState, page: 1 })),

  setCategory: (category) => set((state) => ({ ...state, category, page: 1 })),

  setSearch: (search) => set((state) => ({ ...state, search, page: 1 })),

  setSortBy: (sortBy) => set((state) => ({ ...state, sortBy })),

  setSortDirection: (sortDirection) =>
    set((state) => ({ ...state, sortDirection })),

  reset: () => set(initialState),
}));
