import { SortDirection } from "@/types/enums";
import { cn } from "@/utils/cn";
import { ChevronDown, ChevronUp, ChevronsUpDown } from "lucide-react";
import { HTMLAttributes, ReactNode } from "react";
/** Direction states for the toggle */

interface SortToggleProps {
  /** Content to be displayed alongside the toggle icon */
  children: string | ReactNode;

  /** Current state of the toggle
   * @default "none"
   */
  value: SortDirection;

  /** Callback function triggered when toggle is clicked
   * @param direction - New direction value
   */
  callback: (direction: SortDirection) => void;

  /** Optional tooltip text shown on hover
   * @default undefined
   */
  title?: string;

  /** Size of the chevron icon in pixels
   * @default 16
   */
  iconSize?: number;

  /** Position of the chevron icon relative to content
   * @default "center"
   */
  iconPlacement?: "start" | "center" | "end";
}
const nextToggleState: Record<SortDirection, SortDirection> = {
  none: SortDirection.DESC,
  desc: SortDirection.ASC,
  asc: SortDirection.NONE,
};
/**
 * A toggle component with sort direction indicator
 *
 * @example
 * ```tsx
 * // Basic usage
 * <Toggle value={isActive} callback={handleChange}>
 *   Sort by Name
 * </Toggle>
 *
 * // With custom icon placement and size
 * <Toggle
 *   value={isActive}
 *   callback={handleChange}
 *   iconSize={24}
 *   iconPlacement="end"
 * >
 *   Sort by Date
 * </Toggle>
 * ```
 */
export default function Toggle({
  children,
  id,
  title,
  value,
  iconSize = 16,
  iconPlacement = "center",
  className,
  callback,
}: SortToggleProps & HTMLAttributes<HTMLDivElement>) {
  const handleClick = () => {
    callback(nextToggleState[value]);
  };

  const getIcon = () => {
    switch (value) {
      case SortDirection.ASC:
        return <ChevronUp size={iconSize} />;
      case SortDirection.DESC:
        return <ChevronDown size={iconSize} />;
      case SortDirection.NONE:
        return <ChevronsUpDown size={iconSize} />;
    }
  };
  return (
    <div
      id={id}
      className={cn("inline-flex gap-2 cursor-pointer select-none btn btn-ghost", className)}
      onClick={handleClick}
      title={title}
    >
      <div>{children}</div>
      <div className={`self-${iconPlacement}`}>{getIcon()}</div>
    </div>
  );
}
