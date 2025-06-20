import PageLayout from "@/components/layouts/PageLayout";

import UserTable from "./table";
import { useQuery } from "@tanstack/react-query";
import { UserListToolbar } from "./toolbar";
import { useUserListQueryStore } from "@/stores/userListQueryStore";
import { userService } from "@/api/userService";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { userListQueryKey } from "./userQuery";

export default function ManageUser() {
  useBreadcrumbs([{ label: "Manage User", path: "/manage-user" }]);
  const { page, type, search, sortBy, sortDirection } = useUserListQueryStore();
  const fetchUsers = async () => {
    try {
      const response = await userService.get_user_list(
        page,
        type,
        search,
        sortBy,
        sortDirection
      );
      return response.data;
    } catch {
      return undefined;
    }
  };
  const { data: userResponse, isLoading } = useQuery({
    queryKey: [
      userListQueryKey,
      {
        type,
        search,
        sortBy,
        sortDirection,
        page,
      },
    ],
    queryFn: () => fetchUsers(),
  });
  const isUserLoading = isLoading;
  console.log(userResponse);
  return (
    <PageLayout title="User List">
      <UserListToolbar />
      <UserTable
        id="user-list"
        users={userResponse?.data}
        paginationMeta={userResponse?.meta}
        isLoading={isUserLoading}
        pageSize={import.meta.env.VITE_LIST_PAGE_SIZE}
      ></UserTable>
    </PageLayout>
  );
}
