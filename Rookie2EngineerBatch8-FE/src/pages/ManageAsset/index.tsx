import PageLayout from "@/components/layouts/PageLayout";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useQuery } from "@tanstack/react-query";
import { useAssetListQueryStore } from "@/stores/assetListQueryStore";
import { assetListQueryKey } from "./assetQuery";
import { AssetListToolbar } from "./toolbar";
import AssetTable from "./table";
import { assetService } from "@/api/assetService";

export default function ManageAsset() {
    useBreadcrumbs([{ label: "Manage Asset", path: "/manage-asset" }]);
    const { page, state, category, search, sortBy, sortDirection } = useAssetListQueryStore();
    const fetchAssets = async () => {
        try {
            const response = await assetService.get_asset_list_paginated(
                page,
                state,
                category,
                search,
                sortBy,
                sortDirection
            );
            return response.data;
        } catch {
            return undefined;
        }
    };
    const { data: assetResponse, isLoading } = useQuery({
        queryKey: [
            assetListQueryKey,
            {
                state,
                category,
                search,
                sortBy,
                sortDirection,
                page,
            },
        ],
        queryFn: () => fetchAssets(),
    });
    return (
        <PageLayout title="Manage Asset">
            <AssetListToolbar />
            <AssetTable
                id="asset-list"
                assets={assetResponse?.data}
                paginationMeta={assetResponse?.meta}
                pageSize={import.meta.env.VITE_LIST_PAGE_SIZE}
                isLoading={isLoading}
            ></AssetTable>
        </PageLayout>
    )
}