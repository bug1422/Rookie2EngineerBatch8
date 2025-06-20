import { ReportSortOption, SortDirection } from "@/types/enums";
import Toggle from "@/components/UI/Toggle";
import { Report } from "@/types/report";
import { truncateText } from "@/utils/string";

interface ReportTableProps {
    reports: Report[];
    isLoading: boolean;
    pageSize: number;
    sortBy: ReportSortOption;
    sortDirection: SortDirection;
    onSort: (sortBy: ReportSortOption) => void;
}

const COLUMNS = [
    { key: ReportSortOption.CATEGORY, label: "Category", width: "15%" },
    { key: ReportSortOption.TOTAL, label: "Total", width: "14%" },
    { key: ReportSortOption.ASSIGNED, label: "Assigned", width: "14%" },
    { key: ReportSortOption.AVAILABLE, label: "Available", width: "14%" },
    { key: ReportSortOption.NOT_AVAILABLE, label: "Not Available", width: "14%" },
    { key: ReportSortOption.WAITING_FOR_RECYCLING, label: "Waiting for Recycling", width: "15%" },
    { key: ReportSortOption.RECYCLED, label: "Recycled", width: "14%" },
];

const ROW_HEIGHT = "h-12";
const MAX_LENGTH = 12;

export const ReportTable = ({ reports, isLoading, pageSize, sortBy, sortDirection, onSort }: ReportTableProps) => {
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

    const renderEmptyState = () => (
        <>
            <tr className={ROW_HEIGHT}>
                <td colSpan={COLUMNS.length} className="text-center text-base-content/60 px-4">
                    No reports found
                </td>
            </tr>
            {renderEmptyRows(pageSize - 1)}
        </>
    );

    const renderCell = (column: (typeof COLUMNS)[0], value: string | number) => {
        if (column.key === ReportSortOption.CATEGORY) {
            const displayText = truncateText(value.toString(), MAX_LENGTH);
            return (
                <div className="tooltip tooltip-right tooltip-info" data-tip={value}>
                    {displayText}
                </div>
            );
        }
        return <span className="block">{value}</span>;
    };

    return (
        <div className="overflow-x-auto my-2 rounded-lg border border-base-300">
            <table className="table table-xs w-full">
                <colgroup>
                    {COLUMNS.map((col) => (
                        <col key={col.key} style={{ width: col.width }} />
                    ))}
                </colgroup>
                <thead>
                    <tr className={`text-sm md:text-base bg-base-200/50 border-b border-base-300 ${ROW_HEIGHT}`}>
                        {COLUMNS.map((column) => (
                            <th key={column.key} className="text-left px-4">
                                <Toggle
                                    className="p-0 h-auto hover:bg-base-300/10"
                                    value={sortBy === column.key ? sortDirection : SortDirection.NONE}
                                    callback={() => onSort(column.key as ReportSortOption)}
                                >
                                    {column.label}
                                </Toggle>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="bg-base-100 divide-y divide-base-300">
                    {isLoading ? (
                        renderLoadingState()
                    ) : reports.length > 0 ? (
                        <>
                            {reports.map((report, index) => (
                                <tr key={index} className={`hover:bg-base-200/50 transition-colors ${ROW_HEIGHT}`}>
                                    {COLUMNS.map((column) => (
                                        <td key={column.key} className="px-4">
                                            {renderCell(column, report[column.key.toLowerCase() as keyof Report])}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            {renderEmptyRows(pageSize - reports.length)}
                        </>
                    ) : (
                        renderEmptyState()
                    )}
                </tbody>
            </table>
        </div>
    );
};
