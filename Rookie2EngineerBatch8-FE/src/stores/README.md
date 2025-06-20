# Stores Directory

This folder contains state management logic for the application using [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction).  
Each file defines a store or related utilities, following best practices for modular and maintainable state management.

## Guidelines

- Organize stores by feature or domain.
- Keep store logic isolated from UI components.
- Document each store's purpose and usage.
- Use Zustand patterns for creating and updating state.

## Example Structure

```
src/stores/
├── userStore.ts
├── productStore.ts
└── README.md
```

## References

- [State Management in React](https://react.dev/learn/state-management)
- [Zustand Documentation](https://docs.pmnd.rs/zustand/getting-started/introduction)