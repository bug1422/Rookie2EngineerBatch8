from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    category_name: str
    
class CategoryRead(CategoryBase):
    prefix: str
    id: int
    
class CategoryCreate(CategoryBase):
    prefix: Optional[str] = Field(None, max_length=10, description="A short prefix for the category")