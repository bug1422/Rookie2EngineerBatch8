# Modal Component

A flexible and reusable modal dialog component built with DaisyUI and React.

## Features

- Customizable header and body content
- Built-in close button
- Backdrop click to close
- Smooth animations
- Confirmation modal variant
- Responsive design
- Accessible keyboard navigation

## Basic Usage

```tsx
import { Modal } from '@/components/UI/Modal';

function MyComponent() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Modal
      isOpen={isOpen}
      header="Modal Title"
      body="Modal content goes here"
      onClose={() => setIsOpen(false)}
    />
  );
}
```

## Confirmation Modal Usage

```tsx
import { ConfirmationModal } from '@/components/UI/Modal';

function MyComponent() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <ConfirmationModal
      isOpen={isOpen}
      body="Are you sure you want to delete this item?"
      callback={() => handleDelete()}
      onClose={() => setIsOpen(false)}
    />
  );
}
```

## Props

### Modal Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | - | Unique identifier for the modal |
| `isOpen` | `boolean` | `false` | Controls modal visibility |
| `header` | `string \| ReactNode` | - | Content to display in modal header |
| `body` | `string \| ReactNode` | - | Content to display in modal body |
| `className` | `string` | - | Additional CSS classes |
| `closeIconSize` | `number` | `24` | Size of the close icon in pixels |
| `onClose` | `() => void` | - | Handler called when modal is closed |

### ConfirmationModal Props
Extends Modal props with:
| Prop | Type | Description |
|------|------|-------------|
| `callback` | `() => void` | Function to execute on confirmation |

## Styling

The modal uses DaisyUI classes and can be customized using:
- `modal` class for the container
- `modal-box` for the content box
- `modal-backdrop` for the background overlay

## Examples

### Custom Header
```tsx
<Modal
  header={<CustomHeader />}
  body="Content"
  isOpen={isOpen}
  onClose={handleClose}
/>
```

### Custom Body with Form
```tsx
<Modal
  header="Edit User"
  body={<UserForm data={userData} />}
  isOpen={isOpen}
  onClose={handleClose}
/>
```

### Confirmation with Custom Message
```tsx
<ConfirmationModal
  isOpen={isOpen}
  body="This action cannot be undone"
  callback={handleDelete}
  onClose={handleClose}
/>
```