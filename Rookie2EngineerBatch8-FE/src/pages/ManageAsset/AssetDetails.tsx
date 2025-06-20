import { AssetDetail } from "@/types/asset";
import AssetHistoryPaginate from "./AssetHistory";

export interface AssetDetailsProps {
    asset: AssetDetail;
}

export default function AssetDetails({ asset }: AssetDetailsProps) {

    let formattedInstalledDate = 'N/A';
    if (asset.installed_date) {
        const dateObj = new Date(asset.installed_date);
        formattedInstalledDate = Intl.DateTimeFormat("vi-VN").format(dateObj);
    }

    return (
        <div className="grid grid-cols-[120px_1fr] gap-y-4 gap-x-2 text-base">
            <div>Asset Code</div>
            <div className="text-base-content break-words overflow-wrap-anywhere">{asset.asset_code}</div>

            <div>Asset Name</div>
            <div className="text-base-content break-words overflow-wrap-anywhere">{asset.asset_name}</div>

            <div>Category</div>
            <div className="text-base-content break-words overflow-wrap-anywhere">{asset.category.category_name}</div>

            <div>Installed Date</div>
            <div className="text-base-content">
                {formattedInstalledDate}
            </div>

            <div>State</div>
            <div className="text-base-content">{asset.asset_state}</div>

            <div>Specification</div>
            <div className="text-base-content break-words overflow-wrap-anywhere">{asset.specification}</div>

            <div>History</div>
            <AssetHistoryPaginate asset={asset} />
        </div>
    );
}
