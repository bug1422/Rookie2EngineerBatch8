# Assignment PopUp Component

A reusable popup component used in the asset management system to display assignment details in a responsive grid layout. This component is commonly used within modals to show detailed information about asset assignments.

## Props

| Name | Type | Description |
|------|------|-------------|
| value | `MyAssignmentDetail \| AssignmentDetail` | Assignment data including asset and assignment details |
| actionContent | `string \| ReactNode` | Optional action buttons (Accept/Decline/Return) |

## Usage Example

```tsx
import { AssignmentPopUp } from "@/components/UI/PopUp/AssignmentPopUp";

// Inside your component
const ActionButtons = () => (
  <div className="flex gap-2">
    <button className="btn btn-ghost btn-sm btn-circle">
      <Check className="cursor-pointer w-6 h-6" color="red" />
    </button>
    <button className="btn btn-ghost btn-sm btn-circle">
      <X className="cursor-pointer w-6 h-6" />
    </button>
  </div>
);

<AssignmentPopUp 
  value={assignmentDetails}
  actionContent={<ActionButtons />}
/>
```

## Features

### Display Fields
- Asset Information
  - Asset Code
  - Asset Name
  - Specification
- Assignment Details
  - Assigned To
  - Assigned By
  - Assigned Date
  - State
  - Note

### Styling
- Responsive grid layout (3 columns)
- Neutral color scheme with 60% opacity for labels
- Small text size (text-sm)
- Flexible action content placement
- Compatible with DaisyUI components

## Integration
Commonly used with:
- Modal component for detailed views
- Assignment management tables
- Mobile-responsive layouts
