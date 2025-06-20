import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { categoryService } from "@/api/categoryService";
import { CategoryDetail } from "@/types/category";
import toast from "@/components/UI/Toast";
import { AxiosError } from "axios";

export const useCategories = () => {
  const queryClient = useQueryClient();

  // Fetch categories
  const { data: categories = [], isLoading: loading } = useQuery<CategoryDetail[]>({
    queryKey: ["categories"],
    queryFn: async () => {
      const response = await categoryService.get_category_list();
      return response.data;
    },
  });

  // Add category mutation
  const { mutateAsync: addCategory } = useMutation<
    CategoryDetail,
    Error,
    { newCategoryName: string; prefix: string }
  >({
    mutationFn: async ({ newCategoryName, prefix }) => {
      const response = await categoryService.create_category({
        category_name: newCategoryName,
        prefix,
      });
      return response.data;
    },
    onSuccess: (newCategory) => {
      queryClient.setQueryData<CategoryDetail[]>(["categories"], (old = []) => [...old, newCategory]);
      toast({
        content: "Category created successfully",
        alertType: "alert-success",
        duration: 3,
      });
    },
    onError: (error: Error) => {
      let backendMessage = error.message;

      if (isAxiosError(error)) {
        const detail = error.response?.data?.detail;
        if (typeof detail === "object" && detail !== null) {
          backendMessage = detail.message || error.message;
          // Try to parse the message if it looks like a stringified dict
          const match = backendMessage.match(/'message': '([^']+)'/);
          if (match) {
            backendMessage = match[1];
          }
        } else if (typeof detail === "string") {
          // Try to parse the message if it looks like a stringified dict
          const match = detail.match(/'message': '([^']+)'/);
          backendMessage = match ? match[1] : detail;
        }
      }

      toast({
        content: backendMessage || "Failed to create category",
        alertType: "alert-error",
        duration: 5,
      });
    },
  });

  // Wrapper for addCategory to match previous API
  const addCategoryWrapper = async (newCategoryName: string, prefix: string = ""): Promise<boolean> => {
    try {
      await addCategory({ newCategoryName, prefix });
      return true;
    } catch {
      return false;
    }
  };

  return { categories, loading, addCategory: addCategoryWrapper };
};

export default useCategories;

function isAxiosError(error: unknown): error is AxiosError<{ detail?: string | { error?: string; message?: string } }> {
  return (error as AxiosError).isAxiosError !== undefined;
}