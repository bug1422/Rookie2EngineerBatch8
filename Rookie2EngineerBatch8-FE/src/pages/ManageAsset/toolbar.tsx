import FilterInput from "@/components/UI/Input/FilterInput";
import SearchInput from "@/components/UI/Input/SearchInput";
import { useAssetListQueryStore } from "@/stores/assetListQueryStore";
import { AssetState } from "@/types/enums";
import { Link } from "react-router-dom";
import { categoryService } from "@/api/categoryService";
import { useQuery } from "@tanstack/react-query";
import { CategoryDetail } from "@/types/category";

export function AssetListToolbar() {
  const states: string[] = Object.values(AssetState);
  const { state } = useAssetListQueryStore();
  const fetchCategories = async () => {
    try {
      const response = await categoryService.get_category_list();
      const result =
        response.data
          ?.filter((category) => category?.category_name)
          ?.map((category: CategoryDetail) => category.category_name) || [];
      return result;
    } catch (error) {
      console.error("Error fetching categories:", error);
      return [];
    }
  };

  const { data: categories } = useQuery({
    queryKey: ["categories", "names"],
    queryFn: fetchCategories,
    refetchOnMount: true
  });

  const { setState, setSearch, setCategory } = useAssetListQueryStore();

  return (
    <div
      className="flex flex-col gap-4 md:flex-row md:justify-between"
      id="asset-search-toolbar"
    >
      <div className="w-full md:w-auto">
        <FilterInput
          id="asset-state-filter"
          name="state"
          width="w-full md:w-58"
          options={states}
          onChange={(selectedOptions: string[]) => {
            const states = selectedOptions as AssetState[];
            setState(states);
          }}
          defaultSelected={
            state ||
            ([
              AssetState.AVAILABLE,
              AssetState.NOT_AVAILABLE,
              AssetState.ASSIGNED,
            ] as string[])
          }
          isMultiple={true}
        />
      </div>
      <div className="w-full md:w-auto">
        <FilterInput
          id="asset-category-filter"
          name="category"
          width="w-full md:w-58"
          options={categories || []}
          onChange={(selectedOptions: string[]) => {
            const category: string = selectedOptions[0];
            setCategory(category);
          }}
        />
      </div>
      <div className="flex flex-col gap-4 justify-between sm:flex-row sm:items-center sm:gap-4 md:gap-6">
        <SearchInput
          id="asset-search-filter"
          name="search"
          width="w-full md:w-72 lg:w-80"
          onChange={(value: string) => {
            setSearch(value);
          }}
        />
        <Link
          to={`/manage-asset/create-asset`}
          className="btn btn-primary px-4 md:px-6 w-full sm:w-auto whitespace-nowrap"
          id="create-asset-link"
        >
          Create new asset
        </Link>
      </div>
    </div>
  );
}
