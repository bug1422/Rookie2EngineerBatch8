type AcceptedClassName =
  | string
  | undefined
  | null
  | false
  | Record<string, boolean>;

/**
 * @param args -- Class name that needs to be combined
 * @returns A combined string of class names.
 * @example
 * className("btn", "active") // "btn active"
 */

export function cn(...args: Array<AcceptedClassName>): string {
  return args
    .flatMap((arg) => {
      if (typeof arg === "string") return [arg];
      if (typeof arg === "object" && arg !== null) {
        return Object.entries(arg)
          .filter(([, value]) => value)
          .map(([key]) => key);
      }
      return [];
    })
    .join(" ");
}
