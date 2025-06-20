import { Modal } from "@/components/UI/Modal";
import UserDisableModal from "@/components/UI/Modal/UserDisableModal";
import Pagination from "@/components/UI/Pagination";
import Toggle from "@/components/UI/Toggle";
import { useDebounce } from "@/hooks/useDebounce";
import { useUserListQueryStore } from "@/stores/userListQueryStore";
import { SortDirection, UserSortOption } from "@/types/enums";
import { PaginatedResponse, PaginationMeta } from "@/types/meta";
import { UserDetail } from "@/types/user";
import { formatDate } from "@/utils/dateFormat";
import { CircleX, Pencil } from "lucide-react";
import { HTMLAttributes, useState } from "react";
import { Link } from "react-router-dom";
import { userListQueryKey } from "./userQuery";
import { useQueryClient } from "@tanstack/react-query";

interface UserTableProps extends Partial<HTMLAttributes<HTMLDivElement>> {
  users: UserDetail[] | undefined;
  paginationMeta: PaginationMeta | undefined;
  usersInfo?: PaginatedResponse<UserDetail[]>;
  isLoading?: boolean;
  pageSize?: number;
}

export default function UserTable({
  users,
  paginationMeta,
  isLoading = false,
  pageSize,
  ...props
}: UserTableProps) {
  const queryClient = useQueryClient();
  const isEmpty = users === undefined || users.length == 0;
  const { page, sortBy, sortDirection, setSortBy, setSortDirection, setPage } =
    useUserListQueryStore();
  const [currentSortBy, setCurrentSortBy] = useState(sortBy);
  const [currentSortDirection, setCurrentSortDirection] =
    useState(sortDirection);
  const [isModalOpen, setModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserDetail | null>(null);
  const refetchUserList = () => {
    queryClient.invalidateQueries({
      queryKey: [userListQueryKey],
    });
  };

  const debouncedSet = useDebounce<[UserSortOption, SortDirection], void>(
    (key: UserSortOption, direction: SortDirection) => {
      setSortBy(key);
      setSortDirection(direction);
      console.log("update");
    },
    300
  );
  const handleToggle = (key: UserSortOption, direction: SortDirection) => {
    setCurrentSortBy(key);
    setCurrentSortDirection(direction);
    debouncedSet(key, direction);
  };
  const handleSelectUser = (detail: UserDetail) => {
    setSelectedUser(detail);
    setModalOpen(true);
  };
  const UserDetailBody = ({ user }: { user: UserDetail | null }) => {
    if (user === null) return "No User Found";
    return (
      <div className="relative grid grid-cols-3 gap-y-2 text-neutral/60">
        <div className="absolute right-0 flex flex-col gap-2 md:hidden">
          <Link to={`/manage-user/${user.id}`} className=" btn btn-ghost">
            <Pencil
              size={24}
              className="w-8 h-8 cursor-pointer py-1"
              stroke="white"
              fill="currentColor"
            />
          </Link>
          <div onClick={(e) => e.stopPropagation()}>
            <UserDisableModal
              userId={user.id}
              validMessage="Are you sure you want to disable this user?"
              invalidMessage="There are valid assignments belonging to this user. Please close all assignments before disabling user."
              className="btn btn-ghost"
              userName={`${user.username}`}
              callback={() => {
                refetchUserList();

                setModalOpen(false);
              }}
            >
              <CircleX
                size={24}
                color="red"
                className="cursor-pointer w-8 h-8  py-1"
              />
            </UserDisableModal>
          </div>
        </div>
        <div className="col-span-1">Staff Code</div>
        <div className="col-span-2 w-fit">{user.staff_code}</div>
        <div className="col-span-1">Full Name</div>
        <div className="col-span-2 w-fit">
          {user.first_name} {user.last_name}
        </div>

        <div className="col-span-1">Username</div>
        <div className="col-span-2">{user.username}</div>

        <div className="col-span-1">Date of Birth</div>
        <div className="col-span-2">{new Date(user.date_of_birth).toLocaleDateString("en-GB")}</div>

        <div className="col-span-1">Gender</div>
        <div className="col-span-2">{user.gender}</div>

        <div className="col-span-1">Joined Date</div>
        <div className="col-span-2">{new Date(user.join_date).toLocaleDateString("en-GB")}</div>

        <div className="col-span-1">Type</div>
        <div className="col-span-2 uppercase">{user.type}</div>

        <div className="col-span-1">Location</div>
        <div className="col-span-2 uppercase">{user.location}</div>
      </div>
    );
  };

  const renderEmptyRows = (totalRows: number) => {
  const filledRows = users?.length || 0;
  const emptyRowsCount = Math.max(0, totalRows - filledRows);

  if (emptyRowsCount <= 0) return null;

  return Array.from({ length: emptyRowsCount }).map((_, index) => (
    <tr key={`empty-${index}`} className="h-12">
      {Array.from({ length: 6 }).map((_, colIndex) => (
        <td 
          key={`empty-cell-${colIndex}`} 
          className="bg-transparent border-0 px-2 py-3"
        />
      ))}
    </tr>
  ));
};

  return (
    <>
      <Modal
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        header={"Detailed User Information"}
        body={<UserDetailBody user={selectedUser} />}
      />
      <div className=" w-full mt-1 overflow-x-auto my-2 rounded-lg border border-base-300" {...props}>
        <table
          id="user-list-table"
          className="hidden md:table table-sm w-full"
        >
          <colgroup>
            <col className="w-[15%]" />
            <col className="w-[20%]" />
            <col className="w-[15%]" />
            <col className="w-[20%]" />
            <col className="w-[15%]" />
            <col className="w-[15%]" />
          </colgroup>
          <thead>
            <tr id="user-sortbar" className="text-sm md:text-base bg-base-200/50 border-b border-base-300 h-12">
              <th className="text-xs !py-0">
                <Toggle
                  className="!p-0"
                  value={
                    (currentSortBy === UserSortOption.STAFF_CODE &&
                      currentSortDirection) ||
                    SortDirection.NONE
                  }
                  callback={(direction: SortDirection) =>
                    handleToggle(UserSortOption.STAFF_CODE, direction)
                  }
                  iconPlacement="end"
                >
                  Staff Code
                </Toggle>
              </th>
              <th className="text-xs !py-0">
                <Toggle
                  className="!p-0"
                  value={
                    (currentSortBy === UserSortOption.FIRST_NAME &&
                      currentSortDirection) ||
                    SortDirection.NONE
                  }
                  callback={(direction: SortDirection) =>
                    handleToggle(UserSortOption.FIRST_NAME, direction)
                  }
                  iconPlacement="end"
                >
                  Full Name
                </Toggle>
              </th>
              <th className="font-semibold text-sm py-0">Username</th>
              <th className="text-xs !py-0">
                <Toggle
                  className="!p-0"
                  value={
                    (currentSortBy === UserSortOption.JOIN_DATE &&
                      currentSortDirection) ||
                    SortDirection.NONE
                  }
                  callback={(direction: SortDirection) =>
                    handleToggle(UserSortOption.JOIN_DATE, direction)
                  }
                  iconPlacement="end"
                >
                  Joined Date
                </Toggle>
              </th>
              <th className="text-xs !py-0">
                <Toggle
                  className="!p-0"
                  value={
                    (currentSortBy === UserSortOption.TYPE &&
                      currentSortDirection) ||
                    SortDirection.NONE
                  }
                  callback={(direction: SortDirection) =>
                    handleToggle(UserSortOption.TYPE, direction)
                  }
                  iconPlacement="end"
                >
                  Type
                </Toggle>
              </th>
              <th className=""></th>
            </tr>
          </thead>
          <tbody id="user-list-container" className="w-full">
            {isLoading ? (
              <>
                {Array.from({ length: pageSize ? pageSize : 10 }, (_, index) => index + 1).map(
                  (_, index) => (
                    <tr
                      id="user-list-loading"
                      key={index}
                      className="w-full text-sm md:text-base"
                    >
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                      <td className="whitespace-nowrap">
                        <div className="w-2/3 h-6 skeleton"></div>
                      </td>
                    </tr>
                  )
                )}
              </>
            ) : isEmpty ? (
              <>
                <tr className="h-12">
                  <td colSpan={5} className="text-center text-base-content/60 px-4">
                      No data
                  </td>
                </tr>
                {renderEmptyRows(pageSize? pageSize : 10)}
              </>
            ) : (
              <>
                {users.map((user, index) => (
                  <tr
                    key={index}
                    onClick={() => handleSelectUser(user)}
                    className="hover:bg-base-200 transition-colors cursor-pointer"
                  >
                    <td className="whitespace-nowrap">
                      <div className="tooltip" data-tip={user.staff_code}>
                        <span className="truncate">{user.staff_code}</span>
                      </div>
                    </td>
                    <td className="whitespace-nowrap">
                      <div
                        className="tooltip"
                        data-tip={`${user.first_name} ${user.last_name}`}
                      >
                        <span className="truncate">
                          {user.first_name} {user.last_name}
                        </span>
                      </div>
                    </td>
                    <td className="whitespace-nowrap ">
                      <div className="tooltip" data-tip={`${user.username}`}>
                        <span className="truncate">{user.username}</span>
                      </div>
                    </td>
                    <td className="whitespace-nowrap ">
                      <div
                        className="tooltip"
                        data-tip={`${formatDate(user.join_date)}`}
                      >
                        <span className="truncate">
                          {new Date(user.join_date).toLocaleDateString("en-GB")}
                        </span>
                      </div>
                    </td>
                    <td className="uppercase whitespace-nowrap ">
                      <div className="tooltip" data-tip={`${user.type}`}>
                        <span className="truncate">{user.type}</span>
                      </div>
                    </td>
                    <td className="h-2" onClick={(e) => e.stopPropagation()}>
                      <div className="flex justify-start items-center lg:gap-0.5 ">
                        <Link
                          to={`/manage-user/${user.id}`}
                          className="btn btn-sm btn-ghost tooltip"
                          data-tip="Edit User"
                        >
                          <Pencil
                            className="w-4 h-4"
                            stroke="white"
                            fill="currentColor"
                          />
                        </Link>
                        <div className="tooltip" data-tip="Disable User">
                          <UserDisableModal
                            userId={user.id}
                            validMessage="Are you sure you want to disable this user?"
                            invalidMessage="There are valid assignments belonging to this user. Please close all assignments before disabling user."
                            className="btn btn-sm btn-ghost tooltip"
                            data-tip="Edit User"
                            userName={`${user.username}`}
                            callback={() => {
                              refetchUserList();
                            }}
                          >
                            <CircleX color="red" className="w-4 h-4"/>
                          </UserDisableModal>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
                {renderEmptyRows(pageSize || 10)}
              </>
            )}
          </tbody>
        </table>

        <div className="md:hidden">
          <div
            id="sm-user-list-container"
            className="flex flex-col divide-y-1 divide-neutral-content"
          >
            <div
              id="sm-user-sortbar"
              className="w-full my-3 justify-around flex flex-row gap-4"
            >
              <Toggle
                className="p-0"
                value={
                  (currentSortBy === UserSortOption.STAFF_CODE &&
                    currentSortDirection) ||
                  SortDirection.NONE
                }
                callback={(direction: SortDirection) =>
                  handleToggle(UserSortOption.STAFF_CODE, direction)
                }
              >
                Staff Code
              </Toggle>
              <Toggle
                className="p-0"
                value={
                  (currentSortBy === UserSortOption.FIRST_NAME &&
                    currentSortDirection) ||
                  SortDirection.NONE
                }
                callback={(direction: SortDirection) =>
                  handleToggle(UserSortOption.FIRST_NAME, direction)
                }
              >
                Full Name
              </Toggle>
              <Toggle
                className="p-0"
                value={
                  (currentSortBy === UserSortOption.JOIN_DATE &&
                    currentSortDirection) ||
                  SortDirection.NONE
                }
                callback={(direction: SortDirection) =>
                  handleToggle(UserSortOption.JOIN_DATE, direction)
                }
              >
                Joined Date
              </Toggle>
              <Toggle
                className="p-0"
                value={
                  (currentSortBy === UserSortOption.TYPE &&
                    currentSortDirection) ||
                  SortDirection.NONE
                }
                callback={(direction: SortDirection) =>
                  handleToggle(UserSortOption.TYPE, direction)
                }
              >
                Type
              </Toggle>
            </div>
            {isLoading ? (
              <>
                {Array.from({ length: 5 }, (_, index) => index + 1).map(
                  (_, index) => (
                    <div
                      key={index}
                      className="w-full p-4 space-y-2 hover:bg-base-200"
                    >
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-sm text-neutral/70">
                          Staff Code
                        </span>
                        <div className="h-4 w-24 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-sm text-neutral/70">
                          Full Name
                        </span>
                        <div className="h-4 w-32 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-sm text-neutral/70">
                          Username
                        </span>
                        <div className="h-4 w-28 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-sm text-neutral/70">
                          Joined Date
                        </span>
                        <div className="h-4 w-28 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-sm text-neutral/70">
                          Type
                        </span>
                        <div className="h-4 w-16 bg-gray-300 rounded animate-pulse"></div>
                      </div>
                    </div>
                  )
                )}
              </>
            ) : isEmpty ? (
              <div className="w-full text-center text-primary font-bold text-5xl mt-32">
                No User Found!
              </div>
            ) : (
              users.map((user, index) => (
                <div
                  key={index}
                  className="w-full p-4 space-y-2 hover:bg-base-200 transition-colors cursor-pointer active:bg-base-300"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSelectUser(user);
                  }}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-neutral/70">
                      Staff Code
                    </span>
                    <span className="text-sm">{user.staff_code}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-neutral/70">
                      Full Name
                    </span>
                    <span className="text-sm">
                      {user.first_name} {user.last_name}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-neutral/70">
                      Username
                    </span>
                    <span className="text-sm">{user.username}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-neutral/70">
                      Joined Date
                    </span>
                    <span className="text-sm">
                      {formatDate(user.join_date)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-neutral/70">
                      Type
                    </span>
                    <span className="text-sm uppercase">{user.type}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-5">
        <Pagination
          isLoading={paginationMeta == undefined}
          currentPage={page}
          maxPage={paginationMeta?.total_pages}
          onChange={(value: number) => setPage(value)}
        />
      </div>
    </>
  );
}
