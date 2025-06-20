# Pages Directory

This folder contains the main page components for the application. Each page is organized within its own subfolder. The structure for each page is as follows:

- Each page resides in a dedicated folder.
- The main component for the page is `index.tsx`.
- If available, tests for the page are included (e.g., `index.test.tsx`).

## Example Structure

```
src/pages/
├── Home/
│   ├── index.tsx
│   └── index.test.tsx
├── About/
│   └── index.tsx
└── Contact/
    ├── index.tsx
    └── index.test.tsx
```

## Guidelines

- Add new pages by creating a new folder and placing an `index.tsx` file inside.
- Include a test file (`index.test.tsx`) in the same folder if tests are available.
- Keep each page self-contained within its folder.
