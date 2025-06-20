import { CommonInputProps } from "..";
import { Search } from "lucide-react";
import { cn } from "@/utils/cn";
import { KeyboardEvent, useState } from "react";
interface SearchInputProps extends CommonInputProps {
  /** Initial date value in ISO format */
  value?: string;
  /** Callback function when value changes */
  onChange?: (value: string) => void;
  placeholder?: string;
  /** Whether the input is disabled */
  disabled?: boolean;
  /** Whether the input is required */
  required?: boolean;
}

export default function SearchInput({
  id,
  name,
  className,
  value,
  onChange,
  placeholder,
  disabled = false,
  required = false,
  width = "w-32",
  iconSize = 16,
}: SearchInputProps) {
  const [inputValue, setInputValue] = useState<string>(value ?? "");

  const handleSearch = () => {
    onChange?.(inputValue);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key == "Enter") {
      e.preventDefault();
      handleSearch();
    }
  };
  return (
    <div className={cn("join inline-flex", className && className, width)}>
      <input
        type="text"
        className="input"
        id={id}
        name={name}
        value={value}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        title="Search input"
      />
      <div className="join-item btn" onClick={handleSearch}>
        <Search size={iconSize} />
      </div>
    </div>
  );
}
