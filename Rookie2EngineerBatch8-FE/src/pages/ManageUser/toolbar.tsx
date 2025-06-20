import FilterInput from "@/components/UI/Input/FilterInput";
import SearchInput from "@/components/UI/Input/SearchInput";
import { useUserListQueryStore } from "@/stores/userListQueryStore";
import { Type } from "@/types/enums";
import { Link } from "react-router-dom";

export function UserListToolbar() {
  const roles: string[] = Object.keys(Type);
  const { setType, setSearch } = useUserListQueryStore();

  return (
    <div
      id="user-search-toolbar"
      className="flex flex-col gap-4 md:flex-row md:justify-between"
    >
      <div className="w-full md:w-auto">
        <FilterInput
          id="user-role-filter"
          name="role"
          width="w-full md:w-58"
          options={roles}
          onChange={(selectedOptions: string[]) => {
            const type = Type[selectedOptions[0] as keyof typeof Type];
            setType(type);
          }}
        />
      </div>
      <div className="flex flex-col gap-4 justify-between sm:flex-row sm:items-center sm:gap-4 md:gap-6">
        <SearchInput
          id="user-search-filter"
          name="search"
          width="w-full md:w-72 lg:w-80"
          onChange={(value: string) => {
            setSearch(value);
          }}
        />
        <Link
          to={`/manage-user/create-user`}
          className="btn btn-primary px-4 md:px-6 w-full sm:w-auto whitespace-nowrap"
          id="create-user-link"
        >
          Create new user
        </Link>
      </div>
    </div>
  );
}
