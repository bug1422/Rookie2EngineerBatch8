# Breadcrumbs Component

This component displays a breadcrumb navigation bar with customizable chevrons using lucide-react icons. It is designed to work with a global breadcrumbs store (Zustand) and a custom hook for easy integration.

## Features

-   Customizable chevron separator (thicker, using lucide-react)
-   Supports clickable and non-clickable breadcrumb items
-   Responsive and accessible markup
-   Integrates with Zustand store and `useBreadcrumbs` hook

## Usage

1. **Set breadcrumbs in your page/component:**

```tsx
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";

export default function EditUserPage() {
    useBreadcrumbs([{ label: "Manage User", path: "/manage-user" }, { label: "Edit User" }]);
    // ...rest of your component
}
```

2. **Breadcrumbs will automatically display in the Navbar (or wherever the component is used):**

```tsx
import Breadcrumbs from "@/components/UI/Breadcrumbs";

// Inside your layout or navbar:
<Breadcrumbs />;
```

## Example Output

```
Manage User > Edit User
```

## Dependencies

-   [lucide-react](https://lucide.dev/)
-   [Zustand](https://zustand-demo.pmnd.rs/)
