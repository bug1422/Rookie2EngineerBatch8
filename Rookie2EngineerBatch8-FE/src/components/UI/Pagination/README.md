# Pagination Component

A flexible React pagination component with configurable page ranges and navigation controls.

## 🚀 Features

- **Configurable Display**: Control visible pages with `pageOffset`
- **Navigation Controls**: Previous/Next buttons with disabled states
- **Dynamic Range**: Smart page number calculations
- **Responsive Design**: Mobile-first approach
- **TypeScript Support**: Full type definitions included
- **Accessibility**: Keyboard navigation and ARIA labels

## 📦 Installation

```bash
# No additional installation needed - component is internal
```

## 🎯 Quick Start

```tsx
import { useState } from 'react';
import Pagination from '@/components/UI/Pagination';

function MyComponent() {
  const [page, setPage] = useState(1);

  return (
    <Pagination
      currentPage={page}
      maxPage={10}
      pageOffset={1}
      onChange={setPage}
    />
  );
}
```

## 📝 Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `currentPage` | `number` | ✅ | - | Active page (min: 1) |
| `maxPage` | `number` | ✅ | - | Total pages (min: 1) |
| `pageOffset` | `number` | ❌ | 1 | Pages shown on each side |
| `onChange` | `(page: number) => void` | ❌ | - | Page change handler |

## 📚 Examples

### Basic Usage
```tsx
<Pagination
  currentPage={1}
  maxPage={10}
  onChange={handlePageChange}
/>
```

### Custom Page Range
```tsx
// Shows 5 pages: [prev] 1 2 3 4 5 [next]
<Pagination
  currentPage={currentPage}
  maxPage={totalPages}
  pageOffset={2}
  onChange={handlePageChange}
/>
```

### Styled Component
```tsx
<Pagination
  currentPage={currentPage}
  maxPage={totalPages}
  onChange={handlePageChange}
  className="mt-4 shadow-sm rounded-md"
/>
```

## 🎨 Styling

Uses **Tailwind CSS** and **DaisyUI** classes:

```css
/* Base styles */
.pagination-btn {
  @apply btn btn-sm btn-ghost;
}

/* Active page */
.pagination-btn-active {
  @apply btn-primary;
}
```

## 🔍 Page Offset Behavior

The `pageOffset` prop determines the number of visible pages:

| pageOffset | Visual Result | Total Pages Shown |
|------------|---------------|-------------------|
| 1 | `[prev] 1 2 3 [next]` | 3 |
| 2 | `[prev] 1 2 3 4 5 [next]` | 5 |
| 3 | `[prev] 1 2 3 4 5 6 7 [next]` | 7 |

## ⌨️ Keyboard Navigation

- `←` Previous page
- `→` Next page
- `Home` First page
- `End` Last page

## 🚨 Common Pitfalls

1. Ensure `currentPage` is within valid range
2. Handle `onChange` for page updates
3. Consider mobile viewport when setting `pageOffset`
4. Test edge cases (first/last pages)

## 📱 Responsive Behavior

- **Mobile**: Bottom-fixed, centered
- **Tablet**: Inline, right-aligned
- **Desktop**: Standard positioning

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Open pull request

## 📄 License

MIT © [Your Name]