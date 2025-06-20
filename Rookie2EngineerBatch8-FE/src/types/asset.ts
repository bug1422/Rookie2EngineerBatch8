import { SortDirection, AssetSortOption, AssetState } from "./enums";
import { CategoryDetail } from "./category";

export interface AssetBase {
    id: number;
    asset_code: string;
    asset_name: string;
    category: CategoryDetail;
    asset_state: AssetState;
}

export interface AssetDetail extends AssetBase{
    specification: string;
    installed_date: Date;
    asset_location: string;
}

export interface AssetHistory {
    id: number,
    assign_date: Date;
    assigned_to: string;
    assigned_by: string;
    return_date: Date | null;
}

export interface AssetListQueryParams {
  page: number;
  state: AssetState[] | null;
  category: string | null;
  search: string | null;
  sortBy: AssetSortOption | null;
  sortDirection: SortDirection | null;
}

export interface AssetUpdate extends Pick<AssetBase, "asset_name" | "asset_state"> {
    specification: string;
    installed_date: Date;
}

export const AssetUpdatableStates = Object.values(AssetState).filter((state)=> state != AssetState.ASSIGNED) 
export interface Asset {
    asset_name?: string;
    category_id?: number;
    specification?: string;
    installed_date?: Date;
    state?: StateType; 
}

export interface AssetCreate {
    asset_name?: string;
    category_id?: number;
    specification?: string;
    installed_date?: Date;
    asset_state?: StateType;
}

export const StateType = {
    AVAILABLE: "Available",
    NOT_AVAILABLE: "Not Available",
} as const;

export type StateType = typeof StateType[keyof typeof StateType];

export interface AssetDetail {
    id: number;
    asset_code: string;
    asset_name: string;
    category: CategoryDetail;
    specification: string;
    installed_date: Date;
    state?: AssetState;
    location?: string;
}

export interface AssetUpdateForm {
    asset_code: string;
    asset_name: string;
    category: string;
    specification?: string;
    installed_date?: string;
    state?: string;
    location?: string;
}
