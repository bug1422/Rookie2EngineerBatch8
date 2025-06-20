# Enums

This directory contains enumeration types used throughout the application. Enums help maintain consistency and type safety for predefined sets of values.

## Structure

```python
from enum import Enum, auto
from typing import List

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

    @classmethod
    def get_roles_hierarchy(cls) -> List[str]:
        """Get roles in hierarchical order."""
        return [cls.ADMIN.value, cls.MANAGER.value, cls.USER.value]

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

    @classmethod
    def get_active_statuses(cls) -> List[str]:
        """Get statuses that represent active orders."""
        return [cls.PENDING.value, cls.PROCESSING.value]

class AssetType(str, Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    LICENSE = "license"
    PERIPHERAL = "peripheral"
```

## Usage Examples

### In Models

```python
from sqlmodel import SQLModel, Field
from enums.user import UserRole
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### In Schemas

```python
from pydantic import BaseModel
from enums.order import OrderStatus
from typing import Optional

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None

    class Config:
        use_enum_values = True
```

### In API Routes

```python
from fastapi import APIRouter, Depends
from enums.asset import AssetType
from typing import List

router = APIRouter()

@router.get("/assets/{asset_type}")
async def get_assets_by_type(
    asset_type: AssetType,
    current_user: User = Depends(get_current_user)
) -> List[AssetResponse]:
    return await asset_service.get_by_type(asset_type)
```

### In Business Logic

```python
from enums.user import UserRole
from fastapi import HTTPException, status

def check_user_permission(user: User, required_role: UserRole) -> bool:
    """Check if user has required role or higher."""
    roles_hierarchy = UserRole.get_roles_hierarchy()
    user_role_index = roles_hierarchy.index(user.role.value)
    required_role_index = roles_hierarchy.index(required_role.value)
    return user_role_index <= required_role_index

async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    user: User
) -> Order:
    if new_status == OrderStatus.CANCELLED:
        if not check_user_permission(user, UserRole.MANAGER):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers can cancel orders"
            )
    # Process order status update
```

## Best Practices

1. Naming Conventions:
   - Use PascalCase for enum class names
   - Use SCREAMING_SNAKE_CASE for enum values
   - Use descriptive names that reflect the purpose

2. Type Safety:
   - Inherit from `str` for string enums
   - Use `auto()` for numeric enums
   - Add type hints where enums are used

3. Documentation:
   - Document enum classes and values
   - Include examples in docstrings
   - Explain any special behavior

4. Helper Methods:
   - Add class methods for common operations
   - Include validation methods
   - Provide conversion utilities

## Common Patterns

### Status Transitions

```python
from enum import Enum
from typing import Set, Dict

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @classmethod
    def get_allowed_transitions(cls) -> Dict[str, Set[str]]:
        """Get allowed status transitions."""
        return {
            cls.NEW.value: {
                cls.IN_PROGRESS.value,
                cls.CANCELLED.value
            },
            cls.IN_PROGRESS.value: {
                cls.REVIEW.value,
                cls.CANCELLED.value
            },
            cls.REVIEW.value: {
                cls.IN_PROGRESS.value,
                cls.COMPLETED.value
            },
            cls.COMPLETED.value: set(),
            cls.CANCELLED.value: set()
        }

    def can_transition_to(self, new_status: 'TaskStatus') -> bool:
        """Check if status can transition to new status."""
        transitions = self.get_allowed_transitions()
        return new_status.value in transitions[self.value]
```

### Enum with Properties

```python
from enum import Enum
from typing import Optional

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"

    @property
    def display_name(self) -> str:
        """Get user-friendly display name."""
        return {
            self.CREDIT_CARD: "Credit Card",
            self.DEBIT_CARD: "Debit Card",
            self.BANK_TRANSFER: "Bank Transfer",
            self.CRYPTO: "Cryptocurrency"
        }[self]

    @property
    def processing_fee(self) -> float:
        """Get processing fee percentage."""
        return {
            self.CREDIT_CARD: 2.9,
            self.DEBIT_CARD: 1.5,
            self.BANK_TRANSFER: 1.0,
            self.CRYPTO: 0.5
        }[self]

    @property
    def requires_verification(self) -> bool:
        """Check if payment method requires verification."""
        return self in {self.CREDIT_CARD, self.DEBIT_CARD}
```

### Composite Enums

```python
from enum import Flag, auto

class Permissions(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = READ | WRITE | DELETE

    def has_permission(self, permission: 'Permissions') -> bool:
        """Check if permissions include specific permission."""
        return self & permission == permission

# Usage
user_permissions = Permissions.READ | Permissions.WRITE
can_delete = user_permissions.has_permission(Permissions.DELETE)  # False
can_write = user_permissions.has_permission(Permissions.WRITE)    # True
```
