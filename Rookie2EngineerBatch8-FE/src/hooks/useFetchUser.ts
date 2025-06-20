import { userService } from "@/api/userService";
import { useQuery } from "@tanstack/react-query";

export function useFetchUserById(userId: number) {
  // Use React Query to fetch user data
  return useQuery({
    queryKey: ["user", userId],
    queryFn: async () => {
      try {
        const response = await userService.check_valid_user(userId);
        return response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    enabled: false, // Prevent automatic fetching
    retry: false, // Don't retry on failure
  });
}
