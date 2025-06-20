import { Search } from "lucide-react";
import Pagination from "@/components/UI/Pagination";
import { assetService } from "@/api/assetService";
import { useQuery } from "@tanstack/react-query";
import { useSelectAssetModalStore } from "@/stores/selectAssetModalStore";
import { AssetDetail } from "@/types/asset";
import Toggle from "@/components/UI/Toggle";
import { SortDirection } from "@/types/enums";
import { useState } from "react";
import { useDebounce } from "@/hooks/useDebounce";
import { AssetSortOption } from "@/types/enums";

export default function SelectAssetModalBody() {
    const PAGE_SIZE = 5;
    const {
        page,
        search,
        sortBy,
        sortDirection,
        selectedAsset,
        setPage,
        setSearch,
        setSortBy,
        setSortDirection,
        setSelectedAsset,
    } = useSelectAssetModalStore();

    const [searchTerm, setSearchTerm] = useState(search || "");

    const { data: assetResponseData, isLoading } = useQuery({
        queryKey: ["assets", page, search, sortBy, sortDirection, PAGE_SIZE],
        queryFn: () =>
            assetService.get_asset_list(page, PAGE_SIZE, search, sortBy, sortDirection),
    });

    const assets = assetResponseData?.data.data;
    const paginationMeta = assetResponseData?.data.meta;

    const debouncedSetSearch = useDebounce(setSearch, 500);

    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(event.target.value);
    };

    const handleSearchSubmit = () => {
        debouncedSetSearch(searchTerm);
    };

    const handleSort = (newSortBy: AssetSortOption) => {
        if (sortBy === newSortBy) {
            setSortDirection(
                sortDirection === SortDirection.ASC
                    ? SortDirection.DESC
                    : SortDirection.ASC
            );
        } else {
            setSortBy(newSortBy);
            setSortDirection(SortDirection.ASC);
        }
    };

    const handleRowClick = (asset: AssetDetail) => {
        setSelectedAsset({
            id: asset.id,
            assetCode: asset.asset_code,
            assetName: asset.asset_name,
            category: asset.category.category_name,
        });
    };

    const renderEmptyRows = (count: number) => {
        return Array.from({ length: count }).map((_, index) => (
            <tr key={`empty-${index}`} className="h-12 border-b border-base-300">
                <td></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        ));
    };

    return (
        <div className="flex flex-col gap-4 w-full">
            <div className="flex justify-end items-center w-full">
                <div className="join relative w-2/5 max-w-[600px]">
                    <input
                        type="text"
                        placeholder="Search by asset code or name"
                        className="input input-bordered join-item w-full"
                        value={searchTerm}
                        onChange={handleSearchChange}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearchSubmit()}
                    />
                    <button className="btn join-item" onClick={handleSearchSubmit}>
                        <Search />
                    </button>
                </div>
            </div>
            <div className="overflow-x-auto">
                <table className="table table-fixed table-md w-full h-fit table-pin-rows">
                    <colgroup>
                        <col className="w-[5%]" />
                        <col className="w-[30%]" />
                        <col className="w-[35%]" />
                        <col className="w-[30%]" />
                    </colgroup>
                    <thead className="bg-base-200">
                        <tr className="text-sm md:text-base">
                            <th></th>
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === AssetSortOption.ASSET_CODE
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(AssetSortOption.ASSET_CODE)}
                                >
                                    Asset Code
                                </Toggle>
                            </th>
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === AssetSortOption.ASSET_NAME
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(AssetSortOption.ASSET_NAME)}
                                >
                                    Asset Name
                                </Toggle>
                            </th>
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === AssetSortOption.CATEGORY
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(AssetSortOption.CATEGORY)}
                                >
                                    Category
                                </Toggle>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            Array.from({ length: PAGE_SIZE }).map((_, index) => (
                                <tr key={`skeleton-${index}`} className="h-12 border-b border-base-300">
                                    <td><div className="skeleton h-4 w-4 rounded-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                </tr>
                            ))
                        ) : assets && assets.length > 0 ? (
                            <>
                                {assets.map((asset: AssetDetail) => (
                                    <tr
                                        key={asset.id}
                                        onClick={() => handleRowClick(asset)}
                                        className={`h-12 border-b border-base-300 hover:bg-base-200 transition-colors cursor-pointer ${
                                            selectedAsset?.id === asset.id ? "bg-base-300" : ""
                                        }`}
                                    >
                                        <td>
                                            <input
                                                type="radio"
                                                name="select-asset"
                                                className="radio radio-primary"
                                                checked={selectedAsset?.id === asset.id}
                                                onChange={() => handleRowClick(asset)}
                                            />
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{asset.asset_code}</span>
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{asset.asset_name}</span>
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{asset.category.category_name}</span>
                                        </td>
                                    </tr>
                                ))}
                                {renderEmptyRows(Math.max(0, PAGE_SIZE - assets.length))}
                            </>
                        ) : (
                            <>
                                <tr className="h-12 border-b border-base-300">
                                    <td colSpan={4} className="text-center">
                                        No assets found.
                                    </td>
                                </tr>
                                {renderEmptyRows(PAGE_SIZE - 1)}
                            </>
                        )}
                    </tbody>
                </table>
            </div>

            <div className="flex justify-end items-center w-full mt-4">
                <Pagination
                    isLoading={isLoading}
                    currentPage={page}
                    maxPage={paginationMeta?.total_pages || 0}
                    onChange={(newPage) => setPage(newPage)}
                />
            </div>
        </div>
    );
}
