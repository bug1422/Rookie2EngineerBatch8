import PageLayout from "@/components/layouts/PageLayout";

import AssignmentTable from "@/pages/ManageAssignment/table";
import { useQuery } from "@tanstack/react-query";
import { AssignmentListToolbar } from "@/pages/ManageAssignment/toolbar";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { assignmentService } from "@/api/assignmentService";
import { useAssignmentListQueryStore } from "@/stores/assignmentListQueryStore";

const pageSize = import.meta.env.VITE_LIST_PAGE_SIZE;

export default function ManageAssignment() {
  useBreadcrumbs([{ label: "Manage Assignment" }]);

  const {
    page,
    assignmentState,
    assigned_date,
    search,
    sortBy,
    sortDirection,
  } = useAssignmentListQueryStore();
  const fetchAssignments = async () => {
    try {
      const response = await assignmentService.get_assignment_list(
        page,
        undefined,
        undefined,
        assignmentState,
        assigned_date,
        search,
        sortBy,
        sortDirection
      );
      return response.data;
    } catch {
      // Return an empty paginated response instead of undefined
      return {
        data: [],
        meta: {
          page: 1,
          total: 0,
          total_pages: 0,
          pageSize: pageSize
        },
      };
    }
  };

  const { data: assignmentResponse, isLoading } = useQuery({
    queryKey: [
      "assignment-list",
      {
        assignmentState,
        assigned_date,
        page,
        search,
        sortBy,
        sortDirection,
      },
    ],
    queryFn: fetchAssignments,
    // Add retry configuration if needed
    retry: false,
  });
  const isUserLoading = isLoading;
  return (
    <PageLayout title="Assignment List">
      <AssignmentListToolbar />
      <AssignmentTable
        id="assignment-list"
        isLoading={isUserLoading}
        assignmentsInfo={assignmentResponse}
        pageSize={pageSize}
      ></AssignmentTable>
    </PageLayout>
  );
}
