from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.category import CategoryRepository
from schemas.category import CategoryCreate, CategoryRead
from typing import List
from core.logging_config import get_logger
from utils.generator import Generator
from models.category import Category
import re

logger = get_logger(__name__)


class CategoryService:
    def __init__(self, db: Session):
        # Initialize services, pass db to them
        # Yes, you are right, this is "dependency... drilling" - Said Quang Truong
        # Challenge: How to do it better?
        self.repository = CategoryRepository(db)

    def is_validate_category_creation(self, category_data: CategoryCreate) -> dict:
        # Determine prefix (user-provided or generated)
        prefix = (category_data.prefix or Generator.generate_prefix(category_data.category_name))

        # Whitelist: Only allow letters in prefix (case-insensitive)
        if not re.fullmatch(r"[A-Za-z]+", prefix):
            return {
                "valid": False,
                "reason": "Prefix must contain only letters (A-Z, a-z)"
            }

        # Check if category name exists
        if self.repository.is_category_name_exists(category_data.category_name):
            return {"valid": False, "reason": "Category name already exists"}

        # Check if prefix exists
        if self.repository.is_prefix_exists(prefix):
            return {"valid": False, "reason": f"Prefix '{prefix}' already exists"}

        return {
            "valid": True,
            "prefix": prefix
        }

    def get_categories(self) -> List[CategoryRead]:
        try:
            categories = self.repository.get_categories()
            logger.info("Fetched categories successfully")
            return categories
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_category_by_id(self, category_id: int) -> CategoryRead:
        try:
            category = self.repository.get_category_by_id(category_id)
            if not category:
                logger.warning(f"Category with ID {category_id} not found")
                raise HTTPException(status_code=404, detail="Category not found")
            return category
        except Exception as e:
            logger.error(f"Error fetching category by ID: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def update_category(self, category_data: CategoryRead) -> CategoryRead:
        try:
            # Fetch the existing category
            category = self.repository.get_category_by_id(category_data.id)
            if not category:
                logger.error(f"Category with ID {category_data.id} not found")
                raise HTTPException(status_code=404, detail="Category not found")
    
            # Update the category fields
            

            # Commit the changes
            self.repository.update_category(category)
            logger.info(f"Category updated successfully with category: {category}")
            return category
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        

    def create_category(self, category_data: CategoryCreate, user_id: int) -> CategoryRead:
        try:
            validation_result = self.is_validate_category_creation(category_data)
            if not validation_result["valid"]:
                logger.error(f"Validation error creating category: {validation_result['reason']}")
                reason = validation_result["reason"].lower()
                if "special characters" in reason:
                    error_code = "invalid_special_characters"
                    message = validation_result["reason"]
                elif "category" in reason and "prefix" in reason:
                    error_code = "category_and_prefix_existed"
                    message = "Category and Prefix are already existed. Please enter different values"
                elif "category" in reason:
                    error_code = "category_existed"
                    message = "Category is already existed. Please enter a different category"
                elif "prefix" in reason:
                    error_code = "prefix_existed"
                    message = "Prefix is already existed. Please enter a different prefix"
                else:
                    error_code = "invalid_category"
                    message = validation_result["reason"]
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": 400,
                        "error_code": error_code,
                        "message": message
                    }
                )
            new_category = Category(
                category_name=category_data.category_name,
                prefix=validation_result["prefix"],
                id_counter=0
            )
            category = self.repository.create_category(new_category)
            logger.info("Category created successfully")
            return category
        except HTTPException as http_exc:
            # Re-raise HTTPExceptions as is
            raise http_exc
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": 500,
                    "error_code": "internal_server_error",
                    "message": str(e) #hide these sensitive information
                }
            )

   