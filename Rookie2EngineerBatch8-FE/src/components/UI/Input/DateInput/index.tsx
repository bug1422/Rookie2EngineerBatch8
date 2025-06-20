import { useRef } from "react";
import { CommonInputProps } from "..";
import "./date.css";
import { Calendar, CalendarClock, Clock } from "lucide-react";
import { cn } from "@/utils/cn";
/**
 * Type of time input to display
 * @example
 * // Date picker only (default)
 * type="date"
 *
 * // Time picker only
 * type="time"
 *
 * // Date and time picker combined
 * type="datetime-local"
 */
type TimeType = "date" | "time" | "datetime-local";
interface DateInputProps extends CommonInputProps {
  /** Initial date value in ISO format */
  value?: string;
  /** Callback function when date changes */
  onChange?: (date: string) => void;
  /** Minimum selectable date in ISO format */
  min?: string;
  /** Maximum selectable date in ISO format */
  max?: string;
  /** Placeholder text when no date is selected */
  placeholder?: string;
  /** Whether the input is disabled */
  disabled?: boolean;
  /** Whether the input is required */
  required?: boolean;
  /** Type of time input to display
   * @default "date"
   * @see TimeType for available options
   */
  type?: TimeType;
}

export default function DateInput({
  id,
  name,
  className,
  value,
  onChange,
  min,
  max,
  placeholder,
  disabled = false,
  required = false,
  width = "w-32",
  iconSize = 16,
  type = "date",
}: DateInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const handleOpenPicker = () => {
    const input = inputRef.current;
    if (!input) return;
    input.showPicker();
  };
  return (
    <div className={cn("join inline-flex", className && className, width)}>
        <input
          ref={inputRef}
          type={type}
          id={id}
          name={name}
          value={value}
          min={min}
          max={max}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          onChange={(e) => onChange?.(e.target.value)}
          title="Date input"
          className="date-input input bg-base-100 join-item flex-1"
        />
      <div className="join-item btn" onClick={handleOpenPicker}>
        {type == "date" ? (
          <Calendar size={iconSize} />
        ) : type == "time" ? (
          <Clock size={iconSize} />
        ) : (
          type == "datetime-local" && <CalendarClock size={iconSize} />
        )}
      </div>
    </div>
  );
}
