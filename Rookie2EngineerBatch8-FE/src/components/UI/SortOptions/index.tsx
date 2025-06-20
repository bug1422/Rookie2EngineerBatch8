import {
  SortDirection,
} from "@/types/enums";
import Toggle from "../Toggle";
import { ReactNode } from "react";

export interface SortOption<T extends string> {
  key: T;
  label: string;
}

interface SortOptionsProps<T extends string> {
  option: SortOption<T>;
  currentSortBy: T;
  currentSortDirection: SortDirection;
  onToggle: (key: T, direction: SortDirection) => void;
  className?: string;
  toggleClassName?: string;
}

export default function SortOptions<T extends string>({
  option,
  currentSortBy,
  currentSortDirection,
  onToggle,
  className = "",
  toggleClassName = "",
}: SortOptionsProps<T>): ReactNode {
  return (
    <div className={`${className}`}>
      <Toggle
        key={option.key}
        className={`p-0 ${toggleClassName}`}
        value={
          (currentSortBy === option.key && currentSortDirection) ||
          SortDirection.NONE
        }
        callback={(direction: SortDirection) => onToggle(option.key, direction)}
        iconPlacement="end"
      >
        {option.label}
      </Toggle>
    </div>
  );
}
