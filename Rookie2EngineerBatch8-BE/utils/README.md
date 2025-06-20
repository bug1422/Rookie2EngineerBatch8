# Utils

This directory contains utility functions, helpers, and common tools used throughout the application.

## Structure

```
utils/
├── auth.py         # Authentication utilities
├── validators.py   # Custom validators
├── formatters.py   # Data formatting utilities
└── helpers.py      # General helper functions
```

## Authentication Utilities

```python
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

## Validators

```python
from typing import Optional
import re
from pydantic import validator

class Validators:
    @staticmethod
    def validate_phone(v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if not v:
            return v
        pattern = r"^\+?1?\d{9,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

    @staticmethod
    def validate_password(v: str) -> str:
        """
        Validate password strength:
        - At least 8 characters
        - Contains uppercase and lowercase
        - Contains numbers
        - Contains special characters
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letters")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letters")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain numbers")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain special characters")
        return v
```

## Formatters

```python
from datetime import datetime
from typing import Any, Dict

class Formatters:
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime to ISO format."""
        return dt.isoformat()

    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format currency amount."""
        return f"{currency} {amount:,.2f}"

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def format_response(
        data: Any,
        message: str = None,
        status: str = "success"
    ) -> Dict[str, Any]:
        """Format API response."""
        return {
            "status": status,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Helpers

```python
import os
import uuid
from typing import Optional
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class Helpers:
    @staticmethod
    def generate_uuid() -> str:
        """Generate a unique identifier."""
        return str(uuid.uuid4())

    @staticmethod
    def get_current_timestamp() -> datetime:
        """Get current UTC timestamp."""
        return datetime.now(timezone.utc)

    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure directory exists, create if not."""
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete a file if it exists."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False

    @staticmethod
    def chunk_list(lst: list, chunk_size: int) -> list:
        """Split list into chunks of specified size."""
        return [
            lst[i:i + chunk_size]
            for i in range(0, len(lst), chunk_size)
        ]
```

## Pagination Helper

```python
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Query(1, ge=1)
    per_page: int = Query(10, ge=1, le=100)
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page

class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool

def paginate(
    items: List[T],
    params: PaginationParams,
    total: Optional[int] = None
) -> PageResponse[T]:
    """Create paginated response."""
    if total is None:
        total = len(items)
    
    pages = (total + params.per_page - 1) // params.per_page
    
    return PageResponse(
        items=items,
        total=total,
        page=params.page,
        pages=pages,
        has_next=params.page < pages,
        has_prev=params.page > 1
    )
```

## File Handling

```python
import os
from typing import Optional
from fastapi import UploadFile
import aiofiles
import magic

class FileHandler:
    ALLOWED_EXTENSIONS = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf"
    }

    @staticmethod
    async def save_upload_file(
        upload_file: UploadFile,
        destination: str
    ) -> Optional[str]:
        """
        Save uploaded file with proper extension and mime type validation.
        Returns the saved file path or None if validation fails.
        """
        try:
            # Read first chunk for mime type detection
            content = await upload_file.read(2048)
            await upload_file.seek(0)
            
            # Detect mime type
            mime_type = magic.from_buffer(content, mime=True)
            
            # Validate mime type
            if mime_type not in FileHandler.ALLOWED_EXTENSIONS:
                return None
            
            # Generate safe filename
            ext = FileHandler.ALLOWED_EXTENSIONS[mime_type]
            filename = f"{uuid.uuid4()}{ext}"
            filepath = os.path.join(destination, filename)
            
            # Ensure directory exists
            os.makedirs(destination, exist_ok=True)
            
            # Save file
            async with aiofiles.open(filepath, "wb") as f:
                while content := await upload_file.read(1024 * 1024):
                    await f.write(content)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
```

## Best Practices

1. Function Design:
   - Keep functions small and focused
   - Use descriptive names
   - Add type hints
   - Include docstrings
   - Handle errors appropriately

2. Code Organization:
   - Group related utilities
   - Use classes for related methods
   - Keep modules focused
   - Document public interfaces

3. Error Handling:
   - Use appropriate exception types
   - Log errors properly
   - Provide helpful error messages
   - Clean up resources in finally blocks

4. Performance:
   - Cache expensive operations
   - Use generators for large datasets
   - Optimize frequently used functions
   - Use async where appropriate

5. Security:
   - Validate inputs
   - Sanitize file paths
   - Use secure random functions
   - Handle sensitive data carefully
