import { useCallback, useEffect, useRef } from "react";

/**
 * Custom hook to debounce a callback function
 * @param callback - The function to debounce
 * @param delay - Delay in milliseconds
 * @returns A debounced version of the callback function
 *
 * Usage:
 * const debouncedFunction = useDebounce((value) => {
 *   console.log(value);
 * }, 300);
 *
 * // Call debouncedFunction with arguments, it will execute after 300ms of inactivity
 */
export function useDebounce<TParams extends unknown[], TReturn>(
  callback: (...args: TParams) => TReturn,
  delay: number
): (...args: TParams) => void {
  const timerRef = useRef<number>(undefined);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: TParams) => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }

      timerRef.current = setTimeout(() => {
        callback(...args);
      }, delay);
    },
    [callback, delay]
  );
}
