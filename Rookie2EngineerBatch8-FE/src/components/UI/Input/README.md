# Input Components

A collection of reusable input components built with DaisyUI and React.

## Components

### 1. DateInput
A customizable date/time input component with icon trigger.

```tsx
import DateInput from '@/components/UI/Input/DateInput';

// Basic date picker
<DateInput 
  name="date" 
  onChange={(date) => console.log(date)} 
/>

// Time picker
<DateInput 
  type="time"
  name="time" 
/>

// Date and time picker
<DateInput 
  type="datetime-local"
  name="datetime" 
/>
```

### 2. FilterInput
A dropdown filter input with multi-select capabilities.

```tsx
import FilterInput from '@/components/UI/Input/FilterInput';

<FilterInput
  name="Role"
  options={["Admin", "Staff", "User"]}
  defaultSelected={["Admin"]}
/>
```

### 3. SearchInput
A search input field with search icon button.

```tsx
import SearchInput from '@/components/UI/Input/SearchInput';

<SearchInput
  name="search"
  placeholder="Search..."
  onChange={(value) => console.log(value)}
/>
```

## Common Props
All input components share these base props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | - | Unique identifier |
| `name` | `string` | Required | Input field name |
| `className` | `string` | - | Additional CSS classes |
| `width` | `string` | "w-32" | Width class (Tailwind) |
| `iconSize` | `number` | 16 | Size of the icon in pixels |

## Component-Specific Props

### DateInput
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `"date" \| "time" \| "datetime-local"` | "date" | Type of picker |
| `value` | `string` | - | ISO date string |
| `min` | `string` | - | Minimum selectable date |
| `max` | `string` | - | Maximum selectable date |

### FilterInput
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `string[]` | Required | Available filter options |
| `defaultSelected` | `string[]` | all options | Initially selected options |

### SearchInput
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | - | Input value |
| `placeholder` | `string` | - | Placeholder text |
| `disabled` | `boolean` | false | Disable the input |
| `required` | `boolean` | false | Mark as required |

## Styling
- Uses DaisyUI classes for consistent styling
- Customizable through className prop
- Responsive design with Tailwind classes
- Custom icons from Lucide React

## Accessibility
- All inputs are keyboard navigable
- Proper ARIA labels and roles
- Screen reader friendly
- Focus management support