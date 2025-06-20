# Layouts Directory Conventions

This directory contains reusable layout components for the project. Please follow these conventions:

## Naming

- Use **PascalCase** for component filenames (e.g., `MainLayout.jsx`).
- Use descriptive names that reflect the layout's purpose.

## Structure

- Each layout should be in its own folder if it has related assets (styles, tests).
- Keep layout logic separate from page-specific logic.

## Exports

- Export layouts as default exports.

## Documentation

- Add a comment at the top of each layout file describing its purpose.

## Example

```
src/layouts/
    ├── MainLayout.jsx
    └── AuthLayout.jsx
```

## Updates

- Update this README if you introduce new conventions.