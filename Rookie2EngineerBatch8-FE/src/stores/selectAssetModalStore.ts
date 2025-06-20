import { create } from "zustand";
import { AssetSortOption, SortDirection, AssetState } from "@/types/enums";

interface SelectedAssetInfo {
  id: number;
  assetCode: string;
  assetName: string;
  category: string;
}

interface SelectAssetModalState {
  page: number;
  search: string | null;
  sortBy: AssetSortOption | null;
  sortDirection: SortDirection | null;
  selectedAsset: SelectedAssetInfo | null;
  state: AssetState[];
  setPage: (page: number) => void;
  setSearch: (search: string | null) => void;
  setSortBy: (sortBy: AssetSortOption | null) => void;
  setSortDirection: (sortDirection: SortDirection | null) => void;
  setSelectedAsset: (asset: SelectedAssetInfo | null) => void;
  setState: (state: AssetState[]) => void;
  reset: () => void;
}

export const useSelectAssetModalStore = create<SelectAssetModalState>((set) => ({
  page: 1,
  search: null,
  sortBy: null,
  sortDirection: null,
  selectedAsset: null,
  state: [AssetState.AVAILABLE],
  setPage: (page) => set({ page }),
  setSearch: (search) => set({ search, page: 1 }),
  setSortBy: (sortBy) => set({ sortBy, page: 1 }),
  setSortDirection: (sortDirection) => set({ sortDirection, page: 1 }),
  setSelectedAsset: (asset) => set({ selectedAsset: asset }),
  setState: (state) => set({ state }),
  reset: () => set({
    page: 1,
    search: null,
    sortBy: null,
    sortDirection: null,
    selectedAsset: null,
    state: [AssetState.AVAILABLE],
  }),
}));