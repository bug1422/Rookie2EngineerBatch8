import { SortDirection, AssetSortOption, AssetState } from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import { AssetBase, AssetCreate, AssetDetail, AssetHistory, AssetUpdate } from "@/types/asset";
import { IsValid } from "@/types/isValid";
import axiosClient from "@api/axiosClient";

const API_BASE_ROUTE = `/v1/assets`;
const PAGE_SIZE = import.meta.env.VITE_LIST_PAGE_SIZE;

export const assetService = {
  get_asset_list: (
    page: number,
    size?: number,
    search?: string | null,
    sortBy?: AssetSortOption | null,
    sortDirection?: SortDirection | null,
    states?: AssetState[] | null,
  ) => {
    return axiosClient.get<PaginatedResponse<AssetDetail[]>>(
      `${API_BASE_ROUTE}`,
      {
        params: {
          page,
          size: size || PAGE_SIZE,
          search,
          sort_by: sortBy,
          sort_direction: sortDirection,
          states: states || [AssetState.AVAILABLE],
        },
      }
    );
  },

  get_asset_list_paginated: (
    page: number,
    states?: AssetState[] | null,
    category?: string | null,
    search?: string | null,
    sortBy?: AssetSortOption | null,
    sortDirection?: SortDirection | null,
    size?: number,

  ) => {

    const validSortDirection = sortDirection === SortDirection.NONE ? null : sortDirection;

    return axiosClient.get<PaginatedResponse<AssetDetail[]>>(
      `${API_BASE_ROUTE}`,
      {
        params: {
          page,
          states,
          category,
          search,
          sort_by: sortBy,
          sort_direction: validSortDirection,
          size: size || PAGE_SIZE,
        }
      }
    );
  },

  get_asset: (id: number) => {
    return axiosClient.get<AssetDetail>(`${API_BASE_ROUTE}/${id}`);
  },

  update_asset: (id: number, asset: AssetUpdate) => {
    return axiosClient.put<AssetUpdate>(`${API_BASE_ROUTE}/${id}`, asset);
  },

  delete_asset: (
    assetId: number
  ) => {
    return axiosClient.delete<AssetBase>(`${API_BASE_ROUTE}/${assetId}`);
  },

  check_valid_asset: (
    assetId: number
  ) => {
    return axiosClient.get<IsValid>(`${API_BASE_ROUTE}/valid-asset/${assetId}`);
  },

  create_asset: (asset: AssetCreate) => {
    return axiosClient.post<AssetCreate>(`${API_BASE_ROUTE}`, asset);
  },

  get_asset_history: (
    page: number,
    asset_id: number,
    size?: number,
  ) => {
    return axiosClient.get<PaginatedResponse<AssetHistory[]>>(
      `${API_BASE_ROUTE}/${asset_id}/history`,
      {
        params: {
          page: page,
          size: size || 5,
          asset_id: asset_id
        }
      }
    );
  }
};
