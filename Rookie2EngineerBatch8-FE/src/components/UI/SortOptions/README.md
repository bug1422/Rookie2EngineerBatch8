# SortOptions Component

A reusable React component for handling sorting functionality in tables or lists.

## Features

- Generic type support for sort options
- Customizable sort direction (ASC, DESC, NONE)
- Toggleable sort functionality
- Flexible styling through className props

## Props

```typescript
interface SortOptionsProps<T extends string> {
  option: SortOption<T>;        // Sort option configuration
  currentSortBy: T;             // Current sort column
  currentSortDirection: SortDirection; // Current sort direction
  onToggle: (key: T, direction: SortDirection) => void; // Toggle callback
  className?: string;           // Optional container class
  toggleClassName?: string;     // Optional toggle button class
}

interface SortOption<T> {
  key: T;                       // Unique identifier for sort option
  label: string;               // Display label
}
```

## Usage Example

```tsx
const SORT_OPTIONS = [
  { key: MyAssignmentSortOption.ASSET_CODE, label: "Asset Code" },
  { key: MyAssignmentSortOption.ASSET_NAME, label: "Asset Name" },
  // ... more options
];

<SortOptions
  key={option.key}
  option={option}
  currentSortBy={currentSortBy}
  currentSortDirection={currentSortDirection}
  onToggle={handleToggle}
  className="w-full"
  toggleClassName="w-full"
/>
```

## Behavior

- Clicking toggles between ascending, descending, and no sort
- Visual indication of current sort state
- Integrates with Toggle component for consistent UI
- Supports both desktop and mobile layouts

## Dependencies

- Requires Toggle component
- Uses SortDirection enum from types/enums
