from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from typing import List
from schemas.category import CategoryRead, CategoryCreate
from services.category import CategoryService
from schemas.user import UserRead
from api.dependencies import get_current_user
router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=List[CategoryRead],
    status_code=status.HTTP_200_OK,
    summary="Get all categories",
    description="Get a list of all categories."
)
async def get_categories(db: Session = Depends(get_db_session),
                         current_user: UserRead = Depends(get_current_user)):
    """Get all categories"""
    category_service = CategoryService(db)
    return category_service.get_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    summary="Get category by ID",
    description="Get a category by its ID."
)
async def get_category(category_id: int, db: Session = Depends(get_db_session)):
    """Get a category by ID"""
    category_service = CategoryService(db)
    return category_service.get_category_by_id(category_id)


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Create a new category with the provided details.",
    
)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_user)
):
    """Create a new category"""
    category_service = CategoryService(db)
    return category_service.create_category(category, current_user.id)


