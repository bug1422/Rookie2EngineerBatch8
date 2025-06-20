from sqlalchemy.orm import Session
from models.category import Category  # Ensure you have a Category model
from typing import Optional, List
from sqlalchemy.sql import func

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories(self) -> List[Category]:
        """Fetch all categories from the database."""
        return self.db.query(Category).all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Fetch a single category by its ID."""
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_next_id_counter(self, prefix: str) -> int:
        """Get the next id_counter value for a given prefix."""
        last_category = (
            self.db.query(Category)
            .filter(Category.prefix.startswith(prefix))
            .order_by(Category.prefix.desc())
            .first()
        )
        if last_category:
            # Extract the numeric part of the prefix and increment it
            last_number = int(last_category.prefix[len(prefix):])
            return last_number + 1
        return 1

    def create_category(self, category: Category) -> Category:
        """Create a new category"""
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category: Category) -> Category:
        
        self.db.add(category) # when the cateory_id is exist, it will update the category
        
        return category

    def is_category_name_exists(self, category_name: str) -> bool:
        return self.db.query(Category).filter(
            func.lower(Category.category_name) == category_name.lower()
        ).first() is not None

    def is_prefix_exists(self, prefix: str) -> bool:
        return self.db.query(Category).filter(
            func.upper(Category.prefix) == prefix.upper()
        ).first() is not None

   

    
    