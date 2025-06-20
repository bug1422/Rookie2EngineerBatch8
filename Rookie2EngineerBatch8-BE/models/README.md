# Models

This directory contains SQLModel/SQLAlchemy models that represent database tables and their relationships.

## Structure

Each model should be defined in its own file and follow these conventions:

```python
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Guidelines

1. Always include type hints
2. Use appropriate Field constraints (unique, index, etc.)
3. Include created_at and updated_at timestamps
4. Document relationships between models
5. Use appropriate column types
6. Follow naming conventions:
   - Table names: plural, lowercase, underscore_case
   - Model names: singular, PascalCase
   - Column names: singular, lowercase, underscore_case

## Common Field Types

```python
# String fields
name: str = Field(max_length=100)
description: str = Field(max_length=1000, default=None)

# Numeric fields
age: int = Field(ge=0, le=150)
price: float = Field(ge=0)

# Boolean fields
is_active: bool = Field(default=True)

# Date/Time fields
created_at: datetime
due_date: date

# Enum fields
from enum import Enum
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

role: UserRole = Field(default=UserRole.USER)

# Relationships
from typing import List
from sqlmodel import Relationship

# One-to-Many
posts: List["Post"] = Relationship(back_populates="author")

# Many-to-One
author_id: Optional[int] = Field(default=None, foreign_key="users.id")
author: Optional["User"] = Relationship(back_populates="posts")
```

## Example Model with Relationships

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    employees: List["Employee"] = Relationship(back_populates="department")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id")
    department: Optional[Department] = Relationship(back_populates="employees")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```
