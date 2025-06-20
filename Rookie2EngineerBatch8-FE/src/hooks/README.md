# Hooks Directory

This folder contains custom React hooks used throughout the project.

## Naming Conventions

- Hook filenames and function names must start with `use`.
    - Example: `useFetchData.js`, `useAuth.ts`
- Use camelCase for hook names.
    - Example: `useUserProfile`
- Describe the hook's purpose clearly and concisely.
    - Good: `useLocalStorage`
    - Bad: `useThing`

## Example

```js
// useCounter.js
import { useState } from 'react';

export function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);
    const increment = () => setCount(c => c + 1);
    return { count, increment };
}
```

## Guidelines

- Place each hook in its own file.
- Add JSDoc comments to describe the hook's usage and parameters.
- Export hooks as named exports.
