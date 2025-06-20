# Confirmation Modal Component

A reusable confirmation modal component used for confirming user actions, particularly in assignment management workflows.

## Props

| Name | Type | Description |
|------|------|-------------|
| isOpen | `boolean` | Controls the visibility of the modal |
| setOpen | `(open: boolean) => void` | Callback to update modal visibility |
| confirmationText | `string?` | Optional text for confirmation action (e.g., "accept", "decline") |
| onConfirm | `() => void?` | Optional callback function executed on confirmation |

## Usage Example

```tsx
import { ConfirmationModalPopUp } from "@/components/UI/Modal/ConfirmationModal";

// Basic usage
<ConfirmationModalPopUp
  isOpen={isModalOpen}
  setOpen={setModalOpen}
  confirmationText="accept"
  onConfirm={() => {
    // Handle confirmation logic
    console.log("Action confirmed");
  }}
/>

// Usage with assignment actions
<ConfirmationModalPopUp
  isOpen={isRequestModalOpen}
  setOpen={setRequestModalOpen}
  confirmationText="accept"
  onConfirm={() => {
    handleAssignmentAction();
    refetchData();
  }}
/>
```

## Features

### Modal Content
- Dynamic header ("Are you sure?")
- Customizable confirmation message
- Flexible action buttons:
  - Primary action button (uses confirmation text or defaults to "Yes")
  - Cancel button

### Styling
- Uses DaisyUI components
- Error styling for confirmation button
- Responsive design
- Centered content layout
- Capitalized button text

## Common Use Cases
- Accepting/Declining assignments
- Creating return requests
- Confirming asset-related actions
- Any action requiring user confirmation

## Integration
Commonly used with:
- Assignment management tables
- Asset management workflows
- User action confirmations
