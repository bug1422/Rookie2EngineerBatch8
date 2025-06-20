import Toggle from "@/components/UI/Toggle";
import { ReturnRequestSortOption, SortDirection } from "@/types/enums";
import { ReturnRequestResponse } from "@/types/return_request";
import { truncateText } from "@/utils/string";
import { Check } from "lucide-react";
import { X } from "lucide-react";

interface ReturnRequestTableProps {
    requests: ReturnRequestResponse[];
    isLoading: boolean;
    pageSize: number;
    sortBy: ReturnRequestSortOption;
    sortDirection: SortDirection;
    onSort: (sortBy: ReturnRequestSortOption) => void;
    onApprove?: (request: ReturnRequestResponse) => void;
    onCancel?: (request: ReturnRequestResponse) => void;
}

const COLUMNS = [
    {key: ReturnRequestSortOption.ID, label: "No.", width: "8%"},
    {key: ReturnRequestSortOption.ASSET_CODE, label: "Asset Code", width: "10%"},
    {key: ReturnRequestSortOption.ASSET_NAME, label: "Asset Name", width: "15%"},
    {key: ReturnRequestSortOption.REQUESTED_BY, label: "Requested By", width: "10%"},
    {key: ReturnRequestSortOption.ASSIGN_DATE, label: "Assign Date", width: "10%"},
    {key: ReturnRequestSortOption.ACCEPTED_BY, label: "Accepted By", width: "15%"},
    {key: ReturnRequestSortOption.RETURN_DATE, label: "Return Date", width: "10%"},
    {key: ReturnRequestSortOption.STATE, label: "Request State", width: "15%"},
    {key: "actions", label: "Actions", width: "7%"},
]

const ROW_HEIGHT = "h-12";
const MAX_LENGTH = 12;

export const ReturnRequestTable = ({ requests, isLoading, pageSize, sortBy, sortDirection, onSort, onApprove, onCancel }: ReturnRequestTableProps) => {
    const renderLoadingState = () =>
        Array.from({ length: pageSize }).map((_, index) => (
            <tr key={`skeleton-${index}`} className={ROW_HEIGHT}>
                {COLUMNS.map((_, colIndex) => (
                    <td key={colIndex} className="px-4">
                        <div className="flex items-center">
                            <div className="skeleton h-4 w-full bg-base-300"></div>
                        </div>
                    </td>
                ))}
            </tr>
        ));

    const renderEmptyRows = (count: number) => {
        if (count <= 0) return null;
    
        return Array.from({ length: count }).map((_, index) => (
            <tr key={`empty-${index}`} className={ROW_HEIGHT}>
                {COLUMNS.map((_, colIndex) => (
                    <td key={colIndex} className="bg-transparent border-0 px-4"></td>
                ))}
            </tr>
        ));
    };

    const renderEmptyState = () => (
        <>
            <tr className={ROW_HEIGHT}>
                <td colSpan={COLUMNS.length} className="text-center text-base-content/60 px-4">
                    No data
                </td>
            </tr>
            {renderEmptyRows(pageSize - 1)}
        </>
    );

    const renderCell = (column: (typeof COLUMNS)[0], request: ReturnRequestResponse, index?: number) => {
        if (column.key === "No.") {
            return <span className="block">{index !== undefined ? index + 1 : ""}</span>;
        }

        if (column.key === "actions") {
            return renderActionButtons(request);
        }

        let value: string | number | undefined;

        switch (column.key) {
            case ReturnRequestSortOption.ID:
                value = request.id;
                break;
            case ReturnRequestSortOption.ASSET_CODE:
                value = request.asset?.asset_code;
                break;
            case ReturnRequestSortOption.ASSET_NAME:
                value = request.asset?.asset_name;
                break;
            case ReturnRequestSortOption.REQUESTED_BY:
                value = request.requested_by?.username;
                break;
            case ReturnRequestSortOption.ACCEPTED_BY:
                value = request.accepted_by?.username || "-";
                break;
            case ReturnRequestSortOption.ASSIGN_DATE:
                value = request.assignment?.assign_date ? 
                    new Date(request.assignment.assign_date).toLocaleDateString() : "-";
                break;
            case ReturnRequestSortOption.RETURN_DATE:
                value = request.return_date ? 
                    new Date(request.return_date).toLocaleDateString() : "-";
                break;
            case ReturnRequestSortOption.STATE:
                value = request.request_state;
                break;
            default:
                value = undefined;
        }

        if (value === undefined || value === null) {
            return <span className="block">-</span>;
        }

        if (
            column.key === ReturnRequestSortOption.ASSET_CODE ||
            column.key === ReturnRequestSortOption.ASSIGN_DATE ||
            column.key === ReturnRequestSortOption.RETURN_DATE
        ) {
            return <span className="block">{value}</span>;
        }
        
        const displayText = truncateText(value.toString(), MAX_LENGTH);
        return (
            <div className="tooltip tooltip-right tooltip-info" data-tip={value}>
                {displayText}
            </div>
        );
    };

    const renderActionButtons = (request: ReturnRequestResponse) => {
        const isWaitingForReturning = request.request_state === "Waiting for returning";

        return (
            <div className="flex gap-1" onClick={(e) => e.stopPropagation()}>
                <button
                    className={`btn btn-sm btn-ghost ${!isWaitingForReturning ? 'opacity-50 cursor-not-allowed' : ''}`}
                    onClick={() => isWaitingForReturning && onApprove?.(request)}
                    disabled={!isWaitingForReturning}
                    title={isWaitingForReturning ? "Accept return request" : "Cannot accept - request not waiting for return"}
                >
                    <Check
                        size={16}
                        className="w-4 h-4"
                        color={isWaitingForReturning ? "green" : "gray"}
                    />
                </button>
                <button
                    className={`btn btn-sm btn-ghost ${!isWaitingForReturning ? 'opacity-50 cursor-not-allowed' : ''}`}
                    onClick={() => isWaitingForReturning && onCancel?.(request)}
                    disabled={!isWaitingForReturning}
                    title={isWaitingForReturning ? "Cancel return request" : "Cannot cancel - request not waiting for return"}
                >
                    <X
                        size={16}
                        className="w-4 h-4"
                        color={isWaitingForReturning ? "red" : "gray"}
                    />
                </button>
            </div>
        );
    };
    
    return (
        <div className="overflow-x-auto my-2 rounded-lg border border-base-300 max-w-full">
            <table className="table table-xs w-full">
                <colgroup>
                    {COLUMNS.map((col) => (
                        <col key={col.key} style={{ width: col.width }} />
                    ))}
                </colgroup>
                <thead>
                    <tr className={`text-sm md:text-base bg-base-200/50 border-b border-base-300 ${ROW_HEIGHT}`}>
                        {COLUMNS.map((column) => (
                            <th key={column.key} className="text-left">
                                {column.key === "actions" ? (
                                    <span></span>
                                ) : (
                                    <Toggle
                                        className="p-0 h-auto hover:bg-base-300/10"
                                        value={sortBy === column.key ? sortDirection : SortDirection.NONE}
                                        callback={() => onSort(column.key as ReturnRequestSortOption)}
                                    >
                                        {column.label}
                                    </Toggle>
                                )}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {isLoading ? (
                        renderLoadingState() 
                    ) : requests.length === 0 ? (
                        renderEmptyState()
                    ) : (
                        <>
                            {requests.map((request, index) => (
                                <tr key={index} className={`hover:bg-base-200/50 transition-colors ${ROW_HEIGHT}`}>
                                    {COLUMNS.map((column) => (
                                        <td key={column.key}>
                                            {renderCell(column, request, index)}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </>
                    )}
                </tbody>
            </table>
        </div>
    )
}

