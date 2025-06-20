import { Search } from "lucide-react";
import Pagination from "@/components/UI/Pagination";
import { userService } from "@/api/userService";
import { useQuery } from "@tanstack/react-query";
import { useSelectUserModalStore } from "@/stores/selectUserModalStore";
import { UserDetail } from "@/types/user";
import Toggle from "@/components/UI/Toggle";
import { SortDirection, UserSortOption } from "@/types/enums";
import { useState } from "react";
import { useDebounce } from "@/hooks/useDebounce";
import { formatDate } from "@/utils/dateFormat";

export default function SelectUserModalBody() {
    const PAGE_SIZE = 5;
    const {
        page,
        search,
        sortBy,
        sortDirection,
        selectedUser,
        setPage,
        setSearch,
        setSortBy,
        setSortDirection,
        setSelectedUser,
    } = useSelectUserModalStore();

    const [searchTerm, setSearchTerm] = useState(search || "");

    const { data: userResponseData, isLoading } = useQuery({
        queryKey: ["users", page, search, sortBy, sortDirection, PAGE_SIZE],
        queryFn: () =>
            userService.get_user_list(page, null, search, sortBy, sortDirection, PAGE_SIZE),
    });

    const users = userResponseData?.data.data;
    const paginationMeta = userResponseData?.data.meta;

    const debouncedSetSearch = useDebounce(setSearch, 500);

    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(event.target.value);
    };

    const handleSearchSubmit = () => {
        debouncedSetSearch(searchTerm);
    };

    const handleSort = (newSortBy: UserSortOption) => {
        if (sortBy === newSortBy) {
            setSortDirection(
                sortDirection === SortDirection.ASC
                    ? SortDirection.DESC
                    : SortDirection.ASC
            );
        } else {
            setSortBy(newSortBy);
            setSortDirection(SortDirection.ASC);
        }
    };

    const handleRowClick = (user: UserDetail) => {
        setSelectedUser({
            id: user.id,
            firstName: user.first_name,
            lastName: user.last_name,
        });
    };

    const renderEmptyRows = (count: number) => {
        return Array.from({ length: count }).map((_, index) => (
            <tr key={`empty-${index}`} className="h-12 border-b border-base-300">
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        ));
    };

    return (
        <div className="flex flex-col gap-4 w-full">
            <div className="flex justify-end items-center w-full">
                <div className="join relative w-2/5 max-w-[600px]">
                    <input
                        type="text"
                        placeholder="Search by staff code or name"
                        className="input input-bordered join-item w-full"
                        value={searchTerm}
                        onChange={handleSearchChange}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearchSubmit()}
                    />
                    <button className="btn join-item" onClick={handleSearchSubmit}>
                        <Search />
                    </button>
                </div>
            </div>
            {/* User list - table */}
            <div className="overflow-x-auto">
                <table className="table table-fixed table-md w-full h-fit table-pin-rows">
                    <colgroup><col className="w-[5%]" /><col className="w-[20%]" /><col className="w-[30%]" /><col className="w-[25%]" /><col className="w-[20%]" /></colgroup>
                    <thead className="bg-base-200">
                        <tr className="text-sm md:text-base">
                            <th></th>{/* Empty header for radio button column */}
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === UserSortOption.STAFF_CODE
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(UserSortOption.STAFF_CODE)}
                                >
                                    Staff Code
                                </Toggle>
                            </th>
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === UserSortOption.FIRST_NAME
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(UserSortOption.FIRST_NAME)}
                                >
                                    Full Name
                                </Toggle>
                            </th>
                            <th className="text-left">Username</th>{/* Username is not sortable based on ManageUser page */}
                            <th className="text-left">
                                <Toggle
                                    className="p-0"
                                    value={
                                        sortBy === UserSortOption.JOIN_DATE
                                            ? sortDirection!
                                            : SortDirection.NONE
                                    }
                                    callback={() => handleSort(UserSortOption.JOIN_DATE)}
                                >
                                    Joined Date
                                </Toggle>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            Array.from({ length: PAGE_SIZE }).map((_, index) => (
                                <tr key={`skeleton-${index}`} className="h-12 border-b border-base-300">
                                    <td><div className="skeleton h-4 w-4 rounded-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                    <td><div className="skeleton h-4 w-full"></div></td>
                                </tr>
                            ))
                        ) : users && users.length > 0 ? (
                            <>
                                {users.map((user: UserDetail) => (
                                    <tr
                                        key={user.id}
                                        onClick={() => handleRowClick(user)}
                                        className={`h-12 border-b border-base-300 hover:bg-base-200 transition-colors cursor-pointer ${
                                            selectedUser?.id === user.id ? "bg-base-300" : ""
                                        }`}
                                    >
                                        <td>
                                            <input
                                                type="radio"
                                                name="select-user"
                                                className="radio radio-primary"
                                                checked={selectedUser?.id === user.id}
                                                onChange={() => handleRowClick(user)}
                                            />
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{user.staff_code}</span>
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{`${user.first_name} ${user.last_name}`}</span>
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{user.username}</span>
                                        </td>
                                        <td className="whitespace-nowrap">
                                            <span className="truncate block">{formatDate(user.join_date)}</span>
                                        </td>
                                    </tr>
                                ))}
                                {renderEmptyRows(Math.max(0, PAGE_SIZE - users.length))}
                            </>
                        ) : (
                            <>
                                <tr className="h-12 border-b border-base-300">
                                    <td colSpan={5} className="text-center">
                                        No users found.
                                    </td>
                                </tr>
                                {renderEmptyRows(PAGE_SIZE - 1)}
                            </>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Pagination */}
            <div className="flex justify-end items-center w-full mt-4">
                <Pagination
                    isLoading={isLoading}
                    currentPage={page}
                    maxPage={paginationMeta?.total_pages || 0}
                    onChange={(newPage) => setPage(newPage)}
                />
            </div>
        </div>
    );
}
