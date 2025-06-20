import { RequestState } from "@/types/enums";
import { useRequestForReturningListQueryStore } from "@/stores/requestForReturningListQueryStore";
import DateInput from "@/components/UI/Input/DateInput";
import FilterInput from "@/components/UI/Input/FilterInput";
import SearchInput from "@/components/UI/Input/SearchInput";
export function RequestForReturningToolbar() {
    const states: string[] = Object.values(RequestState);
    const { setRequestState, setReturnDate, setSearch } = useRequestForReturningListQueryStore();

    return (
        <div
      id="assignment-search-toolbar"
      className="flex flex-col gap-12 md:flex-row w-full md:justify-between"
    >
      <div className="flex flex-row gap-4 w-full md:w-2/4">
        <FilterInput
          id="assignment-state-filter"
          name="role"
          width="w-1/2"
          options={states}
          onChange={(selectedOptions: string[]) => {
            const state: RequestState = selectedOptions[0] as RequestState;
            setRequestState(state);
          }}
        />
        <DateInput
          id="return-date-filter"
          name="return-date"
          width="w-1/2"
          placeholder="Return Date"
          onChange={(date: string) => {
              // If date is empty, set to null, otherwise create new Date
              setReturnDate(date ? new Date(date) : null);
          }}
        />
      </div>
      <div className="flex flex-col justify-between sm:flex-row sm:items-center sm:gap-2 md:gap-4 w-2/4">
        <SearchInput
          id="request-search-filter"
          name="search"
          width="w-3/4"
          onChange={(value: string) => {
            setSearch(value);
          }}
        />
      </div>
    </div>
    )
}