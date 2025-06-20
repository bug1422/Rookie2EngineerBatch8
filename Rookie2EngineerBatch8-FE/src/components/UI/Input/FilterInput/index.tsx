import { cn } from "@/utils/cn";
import { Funnel } from "lucide-react";
import { useEffect, useState } from "react";
import { CommonInputProps } from "..";

/**
 * Props for the FilterInput component
 * @extends CommonInputProps
 */
interface FilterProps extends CommonInputProps {
  /** Array of options to display in the filter dropdown */
  options: string[];

  /** Array of pre-selected options
   * @default []
   */
  defaultSelected?: string[];

  /** Allow multiple selections
   * @default false
   */
  isMultiple?: boolean;

  /** Callback fired when selection changes
   * @param selectedOptions - Array of currently selected options
   */
  onChange?: (selectedOptions: string[]) => void;
}

export default function FilterInput({
  id,
  name,
  className,
  options,
  defaultSelected,
  isMultiple = false,
  onChange,
  width = "w-32",
  iconSize = 16,
}: FilterProps) {
  const [selectedOpts, setSelectedOpts] = useState<Record<string, boolean>>({});
  defaultSelected = defaultSelected ?? [];
  useEffect(() => {
    const opts: Record<string, boolean> = options.reduce(
      (accumulator, value) => {
        accumulator[value] = defaultSelected.includes(value);
        return accumulator;
      },
      {} as Record<string, boolean>
    );
    setSelectedOpts(opts);
  }, []);
  useEffect(() => {
    const selectedValue = Object.entries(selectedOpts)
      .filter(([, isSelected]) => isSelected)
      .map(([value]) => value);
    onChange?.(selectedValue);
  }, [selectedOpts]);
  const updateSelectedOpts = (value: string) => {
    setSelectedOpts((prev) => {
      let newState = prev;
      if (!isMultiple) {
        newState = Object.keys(newState).reduce(
          (accumulator, key) => ({
            ...accumulator,
            [key]: false,
          }),
          {}
        );
      }
      newState = {
        ...newState,
        [value]: !prev[value],
      };
      return newState;
    });
  };
  const selectedValue = options.filter((p) => selectedOpts[p]);
  const displayValue = selectedValue ? selectedValue.join(",") : name;
  return (
    <div className={cn(className && className, width)}>
      <details
        id={id}
        className={cn("dropdown dropdown-end w-full")}
        aria-label={`Filter Container for ${name}`}
        title={`Filter Container for ${name}`}
      >
        <summary className="join w-full inline-flex">
          <div
            className={cn(
              "input bg-base-100 flex-1 flex items-center join-item"
            )}
          >
            <div className="w-full truncate block ">{displayValue}</div>
          </div>
          <div
            role="button"
            tabIndex={0}
            className="join-item btn "
            aria-label={`Open filter for ${name}`}
            title={`Open filter for ${name}`}
          >
            <Funnel size={iconSize} className="" />
          </div>
        </summary>
        <div className="dropdown-content w-full border-1 border-neutral-content rounded-md">
          {options.map((option: string) => (
            <label
              key={option}
              className="p-1 w-full flex items-center space-x-2 bg-base-100  hover:bg-neutral-content"
            >
              <input
                type="checkbox"
                name={name}
                value={option}
                className="checkbox"
                checked={!!selectedOpts[option]}
                onChange={() => {
                  updateSelectedOpts(option);
                }}
              />
              <span className="">{option}</span>
            </label>
          ))}
        </div>
      </details>
    </div>
  );
}
