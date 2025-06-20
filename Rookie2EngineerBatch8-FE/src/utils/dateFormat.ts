/**
 * Formats a date string or Date object into YYYY-MM-DD format
 * @param dateString - Date string in any valid format or Date object
 * @returns Formatted date string in YYYY-MM-DD format
 * @throws {Error} If dateString is invalid
 * @example
 * // Returns "2024-05-20"
 * formatDate("2024-05-20T00:00:00.000Z")
 * 
 * // Returns "2024/05/20"
 * formatDate(new Date(2024, 4, 20))
 */
export function formatDate(dateString: string | Date): string {
  const date = dateString instanceof Date ? dateString : new Date(dateString);

  // Check if date is valid
  if (isNaN(date.getTime())) {
    throw new Error('Invalid date string provided');
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}/${month}/${day}`;
}