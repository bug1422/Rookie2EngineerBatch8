import DateInput from "@/components/UI/Input/DateInput";
import FilterInput from "@/components/UI/Input/FilterInput";
import SearchInput from "@/components/UI/Input/SearchInput";
import { useAssignmentListQueryStore } from "@/stores/assignmentListQueryStore";
import { AssignmentState } from "@/types/enums";
import { Link } from "react-router-dom";

export function AssignmentListToolbar() {
  const assignmentStates: string[] = Object.values(AssignmentState);
  const { setAssignemtnSate, setAssignedDate, setSearch } =
    useAssignmentListQueryStore();

  return (
    <>
      {/* Desktop */}
      <div
        id="assignment-search-toolbar"
        className="hidden md:flex flex-col gap-12 md:flex-row w-full md:justify-between"
      >
        <div className="flex flex-row gap-4 w-full md:w-2/4">
          <FilterInput
            id="assignment-state-filter"
            name="role"
            width="w-1/2"
            options={assignmentStates}
            onChange={(selectedOptions: string[]) => {
              const state: AssignmentState =
                selectedOptions[0] as AssignmentState;
              setAssignemtnSate(state);
            }}
          />
          <DateInput
            id="assigned-date-filter"
            name="assigned-date"
            width="w-1/2"
            placeholder="Assigned Date"
            onChange={(date: string) => {
              setAssignedDate(date);
            }}
          />
        </div>
        <div className="flex flex-col justify-between sm:flex-row sm:items-center sm:gap-2 md:gap-4 w-2/4">
          <SearchInput
            id="assignment-search-filter"
            name="search"
            width="w-3/4"
            onChange={(value: string) => {
              setSearch(value);
            }}
          />
          <Link
            to={`/manage-assignment/create-assignment`}
            className="btn btn-primary w-1/4 sm:w-auto whitespace-nowrap"
            id="create-assignment-link"
          >
            Create new assignment
          </Link>
        </div>
      </div>

      {/* Mobile */}
      <div className="flex md:hidden flex-col gap-4 w-full items-center mx-4">
        <div className="flex flex-col gap-4">
          <div className="flex flex-row gap-2 w-full">
            <FilterInput
              id="assignment-state-filter-mobile"
              name="role"
              width="w-1/2"
              options={assignmentStates}
              onChange={(selectedOptions: string[]) => {
                const state: AssignmentState =
                  selectedOptions[0] as AssignmentState;
                setAssignemtnSate(state);
              }}
            />
            <DateInput
              id="assigned-date-filter-mobile"
              name="assigned-date"
              width="w-1/2"
              placeholder="Assigned Date"
              onChange={(date: string) => {
                setAssignedDate(date);
              }}
            />
          </div>
          <div className="flex flex-row gap-2 w-full">
            <SearchInput
              id="assignment-search-filter-mobile"
              name="search"
              width="w-1/2"
              onChange={(value: string) => {
                setSearch(value);
              }}
            />
            <Link
              to={`/manage-assignment/create-assignment`}
              className="btn btn-primary w-2/4"
              id="create-assignment-link-mobile"
            >
              Create new assignment
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
