# Utils Folder

This folder contains utility functions and helpers used throughout the project. Utilities are designed to be reusable and modular, supporting various features and components.

## Structure

- Each file provides a specific utility or set of related helpers.
- Utilities should have clear, descriptive names and include JSDoc comments where appropriate.

## Guidelines

- Keep utilities pure and free of side effects when possible.
- Write unit tests for all utility functions.
- Update this README when adding or modifying utilities.

## Example

```js
// exampleUtil.js
/**
 * Capitalizes the first letter of a string.
 * @param {string} str
 * @returns {string}
 */
export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
```