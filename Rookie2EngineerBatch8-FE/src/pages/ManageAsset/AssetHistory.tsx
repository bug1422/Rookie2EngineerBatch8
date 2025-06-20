import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import Pagination from "@/components/UI/Pagination";
import { AssetDetailsProps } from "./AssetDetails";
import { AssetHistory } from "@/types/asset";
import { formatDate } from "@/utils/dateFormat";
import { assetService } from "@/api/assetService";

function AssetHistoryItem({history}: {history: AssetHistory}) {
    return (
        <div className="flex flex-row gap-5 justify-between py-2">
            <div className="w-2/12 text-left border-b border-base-content">{formatDate(history.assign_date)}</div>
            <div className="w-4/12 text-left border-b border-base-content">{history.assigned_to}</div>
            <div className="w-4/12 text-left border-b border-base-content">{history.assigned_by}</div>
            <div className="w-2/12 text-left border-b border-base-content">{history.return_date ? formatDate(history.return_date) : 'Active'}</div>
        </div>
    )
}

function AssetHistoryItemSkeleton() {
    return (
        <div className="flex flex-row gap-5 justify-between py-2">
            <div className="w-2/12 text-left border-b border-base-content">
                <div className="w-full h-6 skeleton"></div>
            </div>
            <div className="w-4/12 text-left border-b border-base-content">
                <div className="w-full h-6 skeleton"></div>
            </div>
            <div className="w-4/12 text-left border-b border-base-content">
                <div className="w-full h-6 skeleton"></div>
            </div>
            <div className="w-2/12 text-left border-b border-base-content">
                <div className="w-full h-6 skeleton"></div>
            </div>
        </div>
    )
}

export default function AssetHistoryPaginate({asset}: AssetDetailsProps) {
    const [historyPage, setHistoryPage] = useState(1);
    const [showSkeleton, setShowSkeleton] = useState(false);
    
    const fetchHistory = async () => {
        try {
            const response = await assetService.get_asset_history(
                historyPage,
                asset.id
            );
            return response.data;
        } catch {
            // Return empty pagination response instead of undefined
            return {
                data: [],
                meta: {
                    page: 1,
                    pageSize: 10,
                    total: 0,
                    total_pages: 1
                }
            };
        }
    };

    const { data: historyResponse, isLoading: isHistoryLoading } = useQuery({
        queryKey: ["asset-history", asset.asset_code, historyPage],
        queryFn: fetchHistory,
    });

    // Handle skeleton display with minimum duration
    useEffect(() => {
        if (isHistoryLoading) {
            setShowSkeleton(true);
        } else {
            // Add a minimum delay of 500ms before hiding skeleton
            const timer = setTimeout(() => {
                setShowSkeleton(false);
            }, 500);

            return () => clearTimeout(timer);
        }
    }, [isHistoryLoading]);

    return (
        <div>
            <div className="flex flex-row gap-5 justify-between">
                <div className="font-bold border-b border-base-content w-2/12 text-left">Assigned Date</div>
                <div className="font-bold border-b border-base-content w-4/12 text-left">Assigned To</div>
                <div className="font-bold border-b border-base-content w-4/12 text-left">Assigned By</div>
                <div className="font-bold border-b border-base-content w-2/12 text-left">Return Date</div>
            </div>
            
            <div className="my-5 min-h-[120px]">
                {showSkeleton ? (
                    Array.from({ length: 3 }, (_, index) => (
                        <AssetHistoryItemSkeleton key={`skeleton-${index}`} />
                    ))
                ) : (
                    (historyResponse?.data?.length ?? 0) > 0 ? (
                        historyResponse?.data?.map((history) => (
                            <AssetHistoryItem key={history.id} history={history} />
                        ))
                    ) : (
                        <div className="text-center text-gray-500 py-8">
                            No history found
                        </div>
                    )
                )}
            </div>
           
            <div className="">
                <Pagination
                    isLoading={showSkeleton}
                    currentPage={historyPage}
                    maxPage={historyResponse?.meta?.total_pages ?? 1}
                    onChange={(value: number) => setHistoryPage(value)}
                />    
            </div>
        </div>
    )
}