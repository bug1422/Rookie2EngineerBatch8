# Types Folder

This folder contains TypeScript type definitions and interfaces used throughout the project. Centralizing types here helps maintain consistency and improves code maintainability.

## Guidelines

- Define all shared types and interfaces in this folder.
- Use descriptive names for type files and exports.
- Update types as the application evolves.

## Structure Example

```
/types
    ├── user.ts
    ├── product.ts
    └── index.ts
```

## File Example

```typescript
// paginatedResponse.ts
interface PaginationMeta {
    total: number;
    page: number;
    total_pages: number;
    size?: number;
}

export interface PaginatedResponse<T> {
    data: T[];
    meta: PaginationMeta;
}
```

## Usage

Import types from this folder wherever needed:

```typescript
import { PaginatedResponse } from '@/types/paginatedResponse';
```