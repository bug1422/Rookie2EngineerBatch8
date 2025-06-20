import { assetService } from "@/api/assetService";
import { useQuery } from "@tanstack/react-query"

export function useFetchClickedAsset(assetId: number){
    return useQuery({
        queryKey: ["asset", assetId],
        queryFn: async () => {
            try {
                const response = await assetService.check_valid_asset(assetId);
                return response.data;
            } catch (error) {
                console.error("Error fetching asset data:", error);
                return { is_valid: false };
            }
        },
        enabled: false,
        retry: false,
    })
}