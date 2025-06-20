/**
 * Generates a 2-letter prefix from a category name.
 * - Removes all non-alphabetic characters.
 * - If only one letter remains, doubles it (e.g., "T-" → "TT").
 * - Otherwise, uses the first two letters.
 * - Returns the prefix in uppercase.
 */
export function getPrefixFromName(name: string): string {
  // Remove non-alphabetic characters and split by spaces
  const words = name
    .split(" ")
    .map(word => word.replace(/[^a-zA-Z]/g, ""))
    .filter(Boolean);

  if (words.length === 0) return "";

  if (words.length === 1) {
    let prefix = words[0].substring(0, 2).toUpperCase();  // Take first two letters
    if (prefix.length === 1) {  // If only one letter, double it
      prefix = prefix + prefix;  // e.g., "L" becomes "LL"
    }
    return prefix.substring(0, 2);  // Ensure it's exactly two letters
  }

  // Take first letter of first and second word
  return (words[0][0] + words[1][0]).toUpperCase();
}
