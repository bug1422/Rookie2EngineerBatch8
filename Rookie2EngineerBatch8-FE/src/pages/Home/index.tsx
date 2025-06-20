import PageLayout from "@/components/layouts/PageLayout";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useQuery } from "@tanstack/react-query";
import { assignmentService } from "@/api/assignmentService";
import {
  useMyAssignemtnListQueryStore,
} from "@/stores/assignmentListQueryStore";
import MyAssignmentTable from "./table";
// import toast from "@/components/UI/Toast";

export default function Home() {
  useBreadcrumbs([{ label: "Home" }]);

  const { page, sortBy, sortDirection } = useMyAssignemtnListQueryStore();
  const fetchUsers = async () => {
    try {
      const response = await assignmentService.get_assign_home_list(
        page,
        sortBy,
        sortDirection
      );
      return response.data;
    } catch {
      return undefined;
    }
  };

  // TODO: Replace with actual user fetching logic
  const { data: myAssignmentResponse, isLoading } = useQuery({
    queryKey: [
      "my-assignment-list",
      {
        page,
        sortBy,
        sortDirection,
      },
    ],
    queryFn: () => fetchUsers(),
  });
  const isMyAssignmentLoading = isLoading;
  return (
    <PageLayout title="My Assignment">
      <MyAssignmentTable
        id="assignment-list"
        isLoading={isMyAssignmentLoading}
        myAssignmentInfo={myAssignmentResponse}
        paginationMeta={myAssignmentResponse?.meta}
        pageSize={import.meta.env.VITE_LIST_PAGE_SIZE}
      ></MyAssignmentTable>
    </PageLayout>
  );
}
