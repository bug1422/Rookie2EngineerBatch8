# Components Structure

Each component should be organized in its own folder. The folder must contain:

- `index.tsx`: The main component file.
- Unit test file (if exists): Should be placed in the same folder, typically named `index.test.tsx` or similar.

## Example Structure

```
src/components/
├── Button/
│   ├── index.tsx
│   └── index.test.tsx
├── Card/
│   └── index.tsx
└── README.md
```

## Guidelines

- **Component Folder**: Create a new folder for each component.
- **Component File**: Name the main file `index.tsx`.
- **Unit Tests**: Place unit tests in the same folder as the component.
- **Documentation**: Update this README to reflect any structural changes.
