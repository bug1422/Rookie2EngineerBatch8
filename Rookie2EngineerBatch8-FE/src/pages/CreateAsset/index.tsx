import PageLayout from "@/components/layouts/PageLayout";
import { assetService } from "@/api/assetService";
import { AssetCreate, StateType } from "@/types/asset";
import { CategoryDetail } from "@/types/category";
import toast from "@/components/UI/Toast";
import React, { useState, useEffect, useRef } from "react";
import { useForm, useController, Control, RegisterOptions } from "react-hook-form";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useNavigate } from "react-router-dom";
import { ChevronDown, Check, X } from "lucide-react";
import useCategories from "@/hooks/useCategory";
import { AxiosError } from "axios";
import { getPrefixFromName } from "@/utils/generateCategoryName";
import { useAssetListQueryStore } from "@/stores/assetListQueryStore";
import { AssetSortOption, SortDirection } from "@/types/enums";

// Utility function to check if input is not only spaces
function isNotOnlySpaces(input: string): boolean {
  return input.trim().length > 0;
}

// **Form Validation Schema**
const validationRules = {
  asset_name: {
    required: "Asset name is required",
    validate: (value: string | undefined) => {
      if (value === undefined || value === null) {
        return "Asset name is required";
      }
      return isNotOnlySpaces(value) ? true : "Asset name cannot be only spaces";
    }
  },
  category_id: {
    required: "Category is required",
    validate: (value: unknown) => {
      return typeof value === "number" && value !== 0 ? true : "Category is required";
    }
  },
  specification: {
    required: "Specification is required",
    validate: (value: string | undefined) => {
      if (value === undefined || value === null) {
        return "Specification is required";
      }
      return isNotOnlySpaces(value) ? true : "Specification cannot be only spaces";
    }
  }
};

const installedDateValidation: RegisterOptions<AssetCreate, "installed_date"> = {
  required: "Installed date is required",
  validate: (value: string | Date | undefined) => {
    let dateValue: Date | undefined;
    if (!value) return "Installed date is required";
    if (typeof value === "string") {
      dateValue = new Date(value);
    } else {
      dateValue = value;
    }
    const today = new Date();
    dateValue.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    return dateValue <= today ? true : "Date cannot be in the future";
  }
};

// **Props Interface for CustomSelectWithInput**
interface CustomSelectWithInputProps {
  name: keyof AssetCreate;
  control: Control<AssetCreate>;
  categories: CategoryDetail[];
  loading?: boolean;
  placeholder?: string;
  onAddNew?: (newCategoryName: string, prefix?: string) => Promise<boolean>;
  disabled?: boolean;
  rules?: RegisterOptions<AssetCreate, keyof AssetCreate>;
}

// **CustomSelectWithInput Component**: A dropdown with input for selecting or adding categories
const CustomSelectWithInput: React.FC<CustomSelectWithInputProps> = ({
  name,
  control,
  categories = [],
  loading = false,
  placeholder = "Select category...",
  onAddNew,
  disabled = false,
  rules
}) => {  
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [prefixValue, setPrefixValue] = useState("");
  const [showInput, setShowInput] = useState(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const {
    field: { value, onChange },
    fieldState: { error }
  } = useController({
    name,
    control,
    rules,
    defaultValue: 0
  });

  const selectedCategory = categories.find(cat => cat.id === value);

  // Handle clicks outside the dropdown to close it
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setShowInput(false);
        setInputValue("");
        setPrefixValue("");
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Focus on the input when it becomes visible
  useEffect(() => {
    if (showInput && inputRef.current) {
      inputRef.current.focus();
    }
  }, [showInput]);

  const handleCategorySelect = (category: CategoryDetail) => {
    onChange(category.id);
    setIsOpen(false);
  };

  const handleAddNewItem = () => {
    setShowInput(true);
  };

  const handleConfirmInput = async () => {
    if (!inputValue.trim()) {
      toast({
        content: "Category name cannot be empty",
        alertType: "alert-error",
        duration: 3,
      });
      return;
    }
    if (onAddNew) {
      const success = await onAddNew(inputValue.trim(), prefixValue.trim());
      if (success) {
        setInputValue("");
        setPrefixValue("");
        setShowInput(false);
        setIsOpen(false);
      }
    }
  };

  const handleCancelInput = () => {
    setInputValue("");
    setPrefixValue("");
    setShowInput(false);
  };

  const handleCategoryNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newName = e.target.value;
    setInputValue(newName);

    // Use the new function to generate the prefix
    setPrefixValue(getPrefixFromName(newName));
  };

  const handlePrefixChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    const lettersOnly = value.replace(/[^a-zA-Z]/g, '');
    setPrefixValue(lettersOnly);
  };

  return (
    <>
      <div className="relative w-full" ref={dropdownRef}>
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className={`input h-10 text-left flex items-center justify-between ${
            error ? 'border-red-500' : 'border-secondary'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          disabled={loading || disabled}
        >
          <span className="text-gray-700">
            {loading ? "Loading..." : selectedCategory?.category_name || placeholder}
          </span>
          <ChevronDown className={`text-secondary transition-transform ${isOpen ? "rotate-180" : ""}`} size={20} />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-secondary rounded shadow-lg z-10 max-h-60 overflow-y-auto">
            {loading ? (
              <div className="p-2 text-gray-500">Loading...</div>
            ) : (
              <>
                {categories.map((category) => (
                  <div
                    key={category.id}
                    onClick={() => handleCategorySelect(category)}
                    className="p-2 hover:bg-gray-100 cursor-pointer flex items-center justify-between text-gray-700"
                  >
                    <span>{category.category_name}</span>
                    {value === category.id && <Check className="text-blue-500" size={16} />}
                  </div>
                ))}
                <div className="border-t border-gray-200">
                  {showInput ? (
                    <div className="p-2 flex items-center bg-gray-50">
                      <input
                        ref={inputRef}
                        type="text"
                        value={inputValue}
                        onChange={handleCategoryNameChange}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") handleConfirmInput();
                          if (e.key === "Escape") handleCancelInput();
                        }}
                        placeholder="Category name..."
                        className="w-48 px-2 py-1 text-sm border border-gray-300 rounded-l focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                      <div className="w-px h-6 bg-gray-300"></div>
                      <input
                        type="text"
                        value={prefixValue}
                        onChange={handlePrefixChange}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") handleConfirmInput();
                          if (e.key === "Escape") handleCancelInput();
                        }}
                        placeholder="Prefix..."
                        maxLength={2}
                        className="w-24 px-2 py-1 text-sm border border-gray-300 rounded-r focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                      <button
                        onClick={handleConfirmInput}
                        type="button"
                        className="p-1 text-green-600 hover:bg-green-100 rounded"
                        disabled={!inputValue.trim()}
                      >
                        <Check size={16} />
                      </button>
                      <button onClick={handleCancelInput} className="p-1 text-red-600 hover:bg-red-100 rounded">
                        <X size={16} />
                      </button>
                    </div>
                  ) : (
                    <div
                      onClick={handleAddNewItem}
                      className="p-2 hover:bg-gray-100 cursor-pointer text-blue-600 text-sm"
                    >
                      + Add new category  
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>
      {error && <p className="text-red-500 text-sm mt-1">{error.message}</p>}
    </>
  );
};

// **CreateAsset Component**: Main form for creating a new asset
export default function CreateAsset() {
  const {setSortBy, setSortDirection } = useAssetListQueryStore()
  const navigate = useNavigate();
  const { categories, loading: categoriesLoading, addCategory } = useCategories();

  const INITIAL_VALUES = {
    asset_name: "",
    category_id: 0,
    specification: "",
    installed_date: new Date().toISOString().split("T")[0],
    asset_state: StateType.AVAILABLE,
  } as unknown as AssetCreate;

  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isValid },
    reset,
    setValue,
  } = useForm<AssetCreate>({
    defaultValues: INITIAL_VALUES,
    mode: "onChange",
  });

  useBreadcrumbs([
    { label: "Manage Asset", path: "/manage-asset" },
    { label: "Create New Asset" },
  ]);

  // Handle adding a new category and updating the form
  const handleAddNewCategory = async (newCategoryName: string, prefix: string = ""): Promise<boolean> => {
    const success = await addCategory(newCategoryName, prefix);
    if (success) {
      const newCategory = categories.find(cat => cat.category_name === newCategoryName);
      if (newCategory) {
        setValue("category_id", newCategory.id);
      }
    }
    return success;
  };

  // Handle form submission
  const onSubmit = async (data: AssetCreate) => {
    try {
      const payload = {
        asset_name: data.asset_name,
        category_id: data.category_id,
        specification: data.specification,
        installed_date: String(data.installed_date),
        asset_state: data.asset_state,
      };
      
      const response = await assetService.create_asset(payload as unknown as AssetCreate);

      if (response.data) {
        toast({
          content: "Asset created successfully, redirecting to previous page",
          alertType: "alert-success",
          duration: 3,
        });
        reset();
        setSortBy(AssetSortOption.UPDATED_DATE)
        setSortDirection(SortDirection.DESC)
        setTimeout(() => {
          navigate(-1);
        }, 3000);
      }
    } catch (error) {
      let backendMessage = "Failed to create asset";

      if (isAxiosError(error)) {
        const response = error.response?.data;
        if (response?.detail && typeof response.detail === "object" && response.detail.message) {
          backendMessage = response.detail.message;
        } else if (response?.detail && typeof response.detail === "string") {
          const detail = response.detail;
          backendMessage = detail.includes(":") ? detail.split(":").pop()?.trim() || detail : detail;
        } else {
          backendMessage = error.message;
        }
      }
      toast({
        content: backendMessage,
        alertType: "alert-error",
        duration: 3,
      });
    }
  };

  const handleCancel = () => {
    navigate(-1);
  };

  return (
    <PageLayout title="Create New Asset">
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md">
        {/* Asset Name Field */}
        <div className="flex items-center mb-4">
          <label htmlFor="asset_name" className="w-1/4">
            Name
          </label>
          <div className="flex flex-col w-3/4">
            <input
              id="asset_name"
              type="text"
              className="input"
              {...register("asset_name", validationRules.asset_name)}
            />
            {errors.asset_name && (
              <p className="textarea-xs text-error">{errors.asset_name.message}</p>
            )}
          </div>
        </div>

        {/* Category Field */}
        <div className="flex items-center mb-4">
          <label htmlFor="category" className="w-1/4">
            Category
          </label>
          <div className="flex flex-col w-3/4">
            <CustomSelectWithInput
              name="category_id"
              control={control}
              categories={categories}
              loading={categoriesLoading}
              placeholder="Select category..."
              onAddNew={handleAddNewCategory}
              rules={validationRules.category_id}
            />
          </div>
        </div>

        {/* Specification Field */}
        <div className="flex items-start mb-4">
          <label className="w-1/4">Specification</label>
          <div className="flex flex-col w-3/4">
            <textarea
              id="specification"
              className="textarea"
              {...register("specification", validationRules.specification)}
            />
            {errors.specification && (
              <p className="textarea-xs text-error">{errors.specification.message}</p>
            )}
          </div>
        </div>

        {/* Installed Date Field */}
        <div className="flex items-center mb-4">
          <label className="w-1/4">Installed Date</label>
          <div className="flex flex-col w-3/4">
            <input
              id="installed_date"
              type="date"
              className="input"
              max={new Date().toISOString().split("T")[0]}
              {...register("installed_date", installedDateValidation)}
            />
            {errors.installed_date && (
              <p className="textarea-xs text-error">{errors.installed_date.message}</p>
            )}
          </div>
        </div>

        {/* State Field */}
        <div className="flex items-start mb-4">
          <label className="w-1/4">State</label>
          <div className="w-3/4">
            {Object.values(StateType).map((state) => (
              <div className="flex items-center gap-2" key={state as string}>
                <input
                  id={`radio-state-${state}`}
                  type="radio"
                  className="radio radio-sm radio-primary"
                  value={state}
                  defaultChecked={state === StateType.AVAILABLE}
                  {...register("asset_state")}
                />
                <label htmlFor={`radio-state-${state}`}>
                  {state as string}
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Form Buttons */}
        <div className="flex justify-end gap-4">
          <button type="submit" className="btn btn-primary" disabled={!isValid}>
            Create
          </button>
          <button
            type="button"
            className="btn btn-secondary btn-outline"
            onClick={handleCancel}
          >
            Cancel
          </button>
        </div>
      </form>
    </PageLayout>
  );
}

// **Utility Function**: Type guard for Axios errors
function isAxiosError(error: unknown): error is AxiosError<{ detail?: string | { error?: string; message?: string }; message?: string }> {
  return (error as AxiosError).isAxiosError !== undefined;
}