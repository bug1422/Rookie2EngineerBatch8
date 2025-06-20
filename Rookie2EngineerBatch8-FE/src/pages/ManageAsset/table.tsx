import { AssetDetail } from "@/types/asset";
import { PaginationMeta } from "@/types/meta";
import { HTMLAttributes, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useDebounce } from "@/hooks/useDebounce";
import { AssetSortOption, AssetState } from "@/types/enums";
import { Modal } from "@/components/UI/Modal";
import { useAssetListQueryStore } from "@/stores/assetListQueryStore";
import { assetListQueryKey } from "./assetQuery";
import AssetDisableModal from "@/components/UI/Modal/AssetDisableModal";
import { Link } from "react-router-dom";
import { CircleX, Pencil } from "lucide-react";
import { SortDirection } from "@/types/enums";
import Toggle from "@/components/UI/Toggle";
import Pagination from "@/components/UI/Pagination";
import AssetDetails from "./AssetDetails";
import "./index.css"
import { cn } from "@/utils/cn";

interface AssetTableProps extends Partial<HTMLAttributes<HTMLDivElement>> {
  assets: AssetDetail[] | undefined;
  paginationMeta: PaginationMeta | undefined;
  isLoading?: boolean;
  pageSize?: number;
}

export default function AssetTable({
    assets,
    paginationMeta,
    isLoading = false,
    pageSize,
    ...props
}: AssetTableProps) {
    const queryClient = useQueryClient();
    const isEmpty = assets === undefined || assets.length == 0;
    const { page, sortBy, sortDirection, setSortBy, setSortDirection, setPage } =
        useAssetListQueryStore();
    const [currentSortBy, setCurrentSortBy] = useState(sortBy);
    const [currentSortDirection, setCurrentSortDirection] =
        useState(sortDirection);
    const [isModalOpen, setModalOpen] = useState(false);
    const [selectedAsset, setSelectedAsset] = useState<AssetDetail | null>(null);
    const refetchAssetList = () => {
        queryClient.invalidateQueries({
            queryKey: [assetListQueryKey],
        });
    };

    const debouncedSet = useDebounce(
        (key: AssetSortOption, direction: SortDirection) => {
            setSortBy(key);
            setSortDirection(direction);
            console.log("update");
        },
        300
    );

    const handleToggle = (key: AssetSortOption, direction: SortDirection) => {
        setCurrentSortBy(key);
        setCurrentSortDirection(direction);
        debouncedSet(key, direction);
    };

    const handleSelectAsset = (detail: AssetDetail) => {
        setSelectedAsset(detail);
        setModalOpen(true);
    };

    const AssetDetailBody = ({ asset }: { asset: AssetDetail | null }) => {
        if (asset == null) return "No Asset Found";
        return (
            <div className="relative p-3 md:p-4">
                <div className="absolute right-0 top-0 flex flex-col gap-2 md:hidden">
                    <Link to={`/manage-asset/${asset.id}`} className="btn btn-ghost">
                        <Pencil
                            size={24}
                            className="w-8 h-8 cursor-pointer py-1"
                            stroke="white"
                            fill="currentColor"
                        />
                    </Link>
                    <div onClick={(e) => e.stopPropagation()}>
                        <AssetDisableModal
                            assetId={asset.id}
                            validMessage="Are you sure you want to delete this asset?"
                            invalidMessage="Cannot delete asset because there are associated historical assignments."
                            className="btn btn-ghost"
                            assetName={`${asset.asset_name}`}
                            callback={() => {
                                refetchAssetList();

                                setModalOpen(false);
                            }}
                        >
                            <CircleX
                                size={24}
                                color="red"
                                className="cursor-pointer w-8 h-8  py-1"
                            />
                        </AssetDisableModal>
                    </div>
                </div>
                {asset && <AssetDetails asset={asset} />}
            </div>
        );
    };

    const renderEmptyRows = (totalRows: number) => {
        const filledRows = assets?.length || 0;
        const emptyRowsCount = Math.max(0, totalRows - filledRows);

        if (emptyRowsCount <= 0) return null;

        return Array.from({ length: emptyRowsCount }).map((_, index) => (
            <tr key={`empty-${index}`} className="h-12">
            {Array.from({ length: 5 }).map((_, colIndex) => (
                <td 
                key={`empty-cell-${colIndex}`} 
                className="bg-transparent border-0 px-2 py-3"
                />
            ))}
            </tr>
        ));
    };

    return (
        <>
            <Modal
                isOpen={isModalOpen}
                onClose={() => setModalOpen(false)}
                header={"Detailed Asset Information"}
                body={<AssetDetailBody asset={selectedAsset} />}
                className="max-w-[60vw]"
            />
            <div className="w-full mt-1 overflow-x-auto my-2 rounded-lg border border-base-300" {...props}>
                <table
                    id="asset-list-table"
                    className="hidden md:table table-sm w-full overflow-y-scroll"
                >
                    {/* Setting up column widths */}
                    <colgroup>
                        <col className="w-[20%]" />
                        <col className="w-[25%]" />
                        <col className="w-[20%]" />
                        <col className="w-[20%]" />
                        <col className="w-[15%]"/>
                    </colgroup>

                    {/* Table header */}
                    <thead>
                        <tr className="text-sm md:text-base bg-base-200/50 border-b border-base-300 h-12">
                            <th className="text-sm !py-0">
                                <Toggle
                                    className="!p-0"
                                    value={
                                        (currentSortBy === AssetSortOption.ASSET_CODE &&
                                            currentSortDirection) ||
                                        SortDirection.NONE
                                    }
                                    callback={(direction: SortDirection) =>
                                        handleToggle(AssetSortOption.ASSET_CODE, direction)
                                    }
                                    iconPlacement="end"
                                >
                                    Asset Code
                                </Toggle>
                            </th>
                            
                            <th className="text-sm !py-0">
                                <Toggle
                                    className="!p-0"
                                    value={
                                        (currentSortBy === AssetSortOption.ASSET_NAME &&
                                            currentSortDirection) ||
                                        SortDirection.NONE
                                    }
                                    callback={(direction: SortDirection) =>
                                        handleToggle(AssetSortOption.ASSET_NAME, direction)
                                    }
                                    iconPlacement="end"
                                >
                                    Asset Name
                                </Toggle>
                            </th>

                            <th className="text-sm !py-0">
                                <Toggle
                                    className="!p-0"
                                    value={
                                        (currentSortBy === AssetSortOption.CATEGORY &&
                                            currentSortDirection) ||
                                        SortDirection.NONE
                                    }
                                    callback={(direction: SortDirection) =>
                                        handleToggle(AssetSortOption.CATEGORY, direction)
                                    }
                                    iconPlacement="end"
                                >
                                    Category
                                </Toggle>
                            </th>

                            <th className="text-sm !py-0">
                                <Toggle
                                    className="!p-0"
                                    value={
                                        (currentSortBy === AssetSortOption.STATE &&
                                            currentSortDirection) ||
                                        SortDirection.NONE
                                    }
                                    callback={(direction: SortDirection) =>
                                        handleToggle(AssetSortOption.STATE, direction)
                                    }
                                    iconPlacement="end"
                                >
                                    State
                                </Toggle>
                            </th>

                            <th id="edit-button-group"></th>
                        </tr>
                    </thead>

                    {/* Table body */}
                    <tbody className="bg-base-100 divide-y divide-base-300" id="asset-list-container">
                        { isLoading ? (
                            <>
                                {Array.from({ length: pageSize || 5 }, (_, index) => index + 1).map(
                                    (_, index) => (
                                        <tr
                                            id="user-list-loading"
                                            key={index}
                                            className="w-full text-sm md:text-base"
                                        >
                                            <td className="whitespace-nowrap">
                                                <div className="w-2/3 h-6 skeleton"></div>
                                            </td>
                                            <td className="whitespace-nowrap">
                                                <div className="w-2/3 h-6 skeleton"></div>
                                            </td>
                                            <td className="whitespace-nowrap">
                                                <div className="w-2/3 h-6 skeleton"></div>
                                            </td>
                                            <td className="whitespace-nowrap">
                                                <div className="w-2/3 h-6 skeleton"></div>
                                            </td>
                                        </tr>
                                    )
                                )}
                            </>
                        ) : isEmpty ? (
                            <>
                                <tr className="h-12">
                                <td colSpan={6} className="text-center text-base-content/60 px-4">
                                    No data
                                </td>
                                </tr>
                                {renderEmptyRows(pageSize || 10)}
                            </>
                        ) : (
                            <>
                                {assets.map((asset) => (
                                    <tr 
                                    key={asset.id} 
                                    onClick={() => handleSelectAsset(asset)} 
                                    className="hover:bg-base-200 transition-colors cursor-pointer text-sm md:text-base"
                                    >
                                        <td className="whitespace-nowrap">
                                            <div className="">{asset.asset_code}</div>
                                        </td>

                                        <td className="whitespace-nowrap overflow-hidden text-ellipsis">
                                            <div className="truncate">{asset.asset_name}</div>
                                        </td>

                                        <td className="whitespace-nowrap">
                                            <div className="">{asset.category.category_name}</div>
                                        </td>

                                        <td className="whitespace-nowrap">
                                            <div className="">{asset.asset_state}</div>
                                        </td>
                                        <td className="flex fustify-start" onClick={(e) => e.stopPropagation()}>
                                            <Link
                                            to={`/manage-asset/${asset.id}`} 
                                            className={cn("btn btn-sm btn-ghost", asset.asset_state == AssetState.ASSIGNED ? "opacity-50" : "" )}
                                            onClick={(e) => asset.asset_state == AssetState.ASSIGNED && e.preventDefault()} // prevent navigating on assigned state
                                            >
                                                <Pencil
                                                    size={24}
                                                    className="w-4 h-4"
                                                    stroke="white"
                                                    fill="currentColor"
                                                />
                                            </Link>
                                            <AssetDisableModal
                                                assetId={asset.id}
                                                validMessage="Are you sure you want to delete this asset?"
                                                invalidMessage="Cannot delete asset because there are associated historical assignments."
                                                className="btn btn-sm btn-ghost"
                                                assetName={`${asset.asset_name}`}
                                                callback={() => {
                                                    refetchAssetList();

                                                    setModalOpen(false);
                                                }}>
                                                <CircleX
                                                    size={24}
                                                    color="red"
                                                    className="cursor-pointer w-4 h-4"
                                                />
                                            </AssetDisableModal>
                                        </td>                                      
                                    </tr>
                                ))}
                                {renderEmptyRows(pageSize || 10)}
                            </>
                        )
                        }
                    </tbody>
                </table>
            </div>
            <div className="mt-5">
                <Pagination
                    isLoading={paginationMeta == undefined}
                    currentPage={page}
                    maxPage={paginationMeta?.total_pages}
                    onChange={(value: number) => setPage(value)}
                />
            </div>
        </>
    )
}