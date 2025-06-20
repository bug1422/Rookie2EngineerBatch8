# Toast Component

A customizable toast notification system for React applications using DaisyUI styling.

## Features

- Multiple toast types (info, success, warning, error)
- Auto-dismiss with configurable duration
- Progress bar indication
- Expandable content on hover
- Slide-in/out animations
- Queue management for multiple toasts

## Usage

```tsx
import toast from '@/components/UI/Toast';

// Basic usage
toast({
  title: "Success",
  content: "Operation completed successfully",
  alertType: "alert-success",
  duration: 3 // seconds
});

// Infinite duration toast
toast({
  title: "Warning",
  content: "Please review the changes",
  alertType: "alert-warning",
  duration: null // Will stay until manually dismissed
});
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | - | Unique identifier for the toast |
| `title` | `string \| ReactNode` | "Toast" | Header text or component |
| `content` | `string \| ReactNode` | - | Main content of the toast |
| `alertType` | `AlertType` | "alert-info" | Visual style of the toast |
| `duration` | `number \| null` | 3 | Auto-dismiss duration in seconds |
| `className` | `string` | - | Additional CSS classes |
| `onDismiss` | `() => void` | - | Callback when toast is dismissed |

## Alert Types

```typescript
type AlertType = 
  | "alert-info"
  | "alert-success"
  | "alert-warning"
  | "alert-error";
```

## Features

- Hover to expand additional content
- Progress bar shows remaining time
- Click to dismiss
- Smooth enter/exit animations
- Stacks multiple toasts
- Queue management
- Auto cleanup

## Implementation Details

The toast system consists of three main parts:
1. Toast Component - Individual toast UI
2. ToastManager - Handles toast queue and rendering
3. Toast Function - Public API for creating toasts

## CSS Customization

Custom animations and styling can be modified in `toast.css`:
- Slide in/out animations
- Progress bar styling
- Toast container positioning