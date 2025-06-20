# Schemas

This directory contains Pydantic models for request/response validation and serialization.

## Structure

Organize schemas by feature and separate request/response models:

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Request Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=100)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)

# Response Models
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Guidelines

1. Use separate models for:
   - Request validation (input)
   - Response serialization (output)
   - Database models (SQLModel)

2. Follow naming conventions:
   - Request models: EntityCreate, EntityUpdate
   - Response models: EntityResponse, EntityList
   - Base models: EntityBase

3. Use appropriate validators:
```python
from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v
```

4. Use Field for validation:
```python
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Product name"
    )
    price: float = Field(
        gt=0,
        description="Product price must be greater than 0"
    )
    quantity: int = Field(
        ge=0,
        description="Product quantity must be non-negative"
    )
```

5. Use Enums for constrained choices:
```python
from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER
```

## Example with Relationships

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base Models
class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class EmployeeBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    department_id: int

# Request Models
class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None

# Response Models
class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DepartmentResponse(DepartmentBase):
    id: int
    employees: List[EmployeeResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Common Validations

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl, constr

class UserProfile(BaseModel):
    # Email validation
    email: EmailStr
    
    # String length and regex
    username: constr(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    
    # Numeric ranges
    age: int = Field(ge=0, le=150)
    
    # URL validation
    website: HttpUrl
    
    # Custom string format
    phone: str = Field(pattern=r"^\+?1?\d{9,15}$")
    
    # Optional fields with defaults
    bio: Optional[str] = Field(
        None,
        max_length=1000,
        description="User biography"
    )
```
