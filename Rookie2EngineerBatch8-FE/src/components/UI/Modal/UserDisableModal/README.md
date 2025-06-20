# UserDisableModal Component

A modal component used for confirming disable user actions.

## Description

The UserDisableModal is a reusable React component that displays a confirmation dialog before disabling a user. It provides a clear interface for administrators to confirm their actions.

## Props

| Prop Name  | Type     | Description                                         |
| ---------- | -------- | --------------------------------------------------- |
| isOpen     | boolean  | Controls the visibility of the modal                |
| onClose    | function | Callback function to handle modal close             |
| onConfirm  | function | Callback function executed when action is confirmed |
| userName   | string   | Name of the user being disabled/enabled             |
| isDisabled | boolean  | Current status of the user account                  |

## Usage

```jsx
import UserDisableModal from "@/components/UI/Modal/UserDisableModal";

function ExamplePage() {
  const handleOnclick = () => {
    console.log("Hello world");
  };
  return (
    <PageLayout title="ExamplePage">
      <UserDisableModal
        userId={1}
        type="valid"
        validMessage="Are you sure you want to disable this user?"
      >
        <button className="btn btn-primary">Disable</button>
      </UserDisableModal>
    </PageLayout>
  );
}
```

## Styling

The component uses Tailwind CSS for styling. All styling is handled through Tailwind utility classes, making it easy to customize the appearance directly in the component's JSX.

## Dependencies

- React
- Tailwind CSS
- Your project's modal system (if any)
