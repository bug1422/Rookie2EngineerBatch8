import { cn } from "@/utils/cn";
import "./toast.css";
import { ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { Check, CircleAlert, CircleX, Info } from "lucide-react";
type AlertType =
  | "alert-info"
  | "alert-success"
  | "alert-warning"
  | "alert-error";
type ToastXPlacement = "toast-start" | "toast-center" | "toast-end";
type ToastYPlacement = "toast-top" | "toast-middle" | "toast-bottom";
interface ToastPosition {
  /** Horizontal placement of the toast
   * @default "toast-center"
   */
  x: ToastXPlacement;

  /** Vertical placement of the toast
   * @default "toast-top"
   */
  y: ToastYPlacement;
}
export interface ToastProps {
  /** Unique identifier for the toast */
  id?: string;
  /** Content to display in the toast */
  content?: string | ReactNode;
  /** Additional CSS classes */
  className?: string;
  /** Type of alert to display
   * @default "alert-info"
   */
  alertType?: AlertType;
  /** Duration in seconds before auto-dismiss
   * @important set to null for unlimited duration
   * @default 3
   */
  duration: number | null;
  /** @deprecated DO NOT USE - Position functionality is not implemented yet
   * @internal This will be removed in future versions
   */
  position?: ToastPosition;
  onDismiss?: () => void;
}
function ToastProgressBar({
  time,
  duration,
}: {
  time: number;
  duration: number;
}) {
  const progressPercent = (time / duration) * 100 - 100;
  const progressionRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (progressionRef.current) {
      progressionRef.current.style.setProperty(
        "--toast-progress",
        `${progressPercent}%`
      );
    }
  }, [progressPercent]);
  return (
    <>
      <div className=" absolute bottom-0 left-0 h-1 bg-current opacity-20 w-full" />
      <div
        ref={progressionRef}
        className="absolute bottom-0 left-0 h-1 bg-current transition-transform duration-100 toast-progress-bar"
      />
    </>
  );
}

function ToastIcon({
  alertType,
  className,
}: {
  alertType: AlertType;
  className: string;
}) {
  return (
    <>
      {alertType === "alert-info" ? (
        <Info className={className} />
      ) : alertType === "alert-success" ? (
        <Check className={className} />
      ) : alertType === "alert-warning" ? (
        <CircleAlert className={className} />
      ) : (
        alertType === "alert-error" && <CircleX className={className} />
      )}
    </>
  );
}

export function Toast({
  id,
  content,
  className,
  alertType = "alert-info",
  duration = 3,
  onDismiss,
}: ToastProps) {
  const [time, setTime] = useState(duration ?? 0);
  const [isClosing, setIsClosing] = useState(false);

  const handleDismiss = useCallback(() => {
    setIsClosing(true);

    setTimeout(() => {
      onDismiss?.();
    }, 300);
  }, [onDismiss]);

  useEffect(() => {
    if (duration == null) return;
    const interval = setInterval(() => {
      setTime((prev) => {
        if (prev <= 0) {
          return 0;
        }
        return prev - 0.1;
      });
    }, 100);

    if (time === 0) {
      clearInterval(interval);
      handleDismiss();
    }

    return () => clearInterval(interval);
  }, [time, duration, handleDismiss]);

  return (
    <div
      id={id}
      onClick={handleDismiss}
      className={cn(
        "alert pb-5 ps-8 pe-12 relative overflow-hidden w-fit min-h-12 max-h-20 z-50 cursor-pointer",
        !isClosing && "group",
        isClosing ? "slide-out-to-top" : "slide-in-from-top",
        alertType,
        className
      )}
    >
      <ToastIcon alertType={alertType} className="absolute left-1" />
      <div className="flex flex-col w-full">
        <div
          className={cn(
            "w-full truncate",
            "group-hover:whitespace-normal group-hover:text-wrap",
            "transition-all duration-200"
          )}
          title={typeof content === "string" ? content : undefined}
        >
          {content}
        </div>
        {duration && <ToastProgressBar time={time} duration={duration} />}
      </div>
    </div>
  );
}
