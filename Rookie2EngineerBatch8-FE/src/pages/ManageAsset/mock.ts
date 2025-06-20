import { AssetState } from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import { AssetDetail } from "@/types/asset";

export const mockCategories = ["Laptop", "Personal Computer", "Monitor", "Network Equipment"];

export const mockAsset: AssetDetail = {
  id: 1,
  asset_code: "LA0001",
  asset_name: "Laptop 1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  category: {
    category_name: "Laptop",
    id: 1,
    prefix: "LA",
  },
  asset_state: AssetState.AVAILABLE,
  specification: "16GB RAM, 512GB SSD aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  installed_date: new Date(),
  asset_location: "Hanoi",
};

const mockAssetList = Array(20).fill(mockAsset);

export const mockAssetsResponse: PaginatedResponse<AssetDetail[]> = {
  data: mockAssetList,
  meta: {
    page: 2,
    pageSize: 20,
    total: 20 * 8,
    total_pages: 8
  }
}
