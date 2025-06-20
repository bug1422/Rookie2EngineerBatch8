from repositories.asset import AssetRepository
from core.logging_config import get_logger
from core.exceptions import NotFoundException, BusinessException
from sqlmodel import Session
from schemas.query.check.isValid import IsValid
from schemas.shared.paginated_response import PaginatedResponse
from schemas.query.filter.asset import AssetFilter
from schemas.asset import AssetRead
from enums.shared.location import Location
from enums.asset.state import AssetState
from fastapi import HTTPException
from schemas.asset import AssetCreate, AssetUpdate
from schemas.user import UserRead
from utils.generator import Generator
from models.asset import Asset
from services.category import CategoryService
from typing import List, Optional
logger = get_logger(__name__)



class AssetService:
    def __init__(self, db: Session):
        self.repository = AssetRepository(db)
        self.db = db
        
    def read_assets_paginated(
        self, states: Optional[List[AssetState]],asset_filter: AssetFilter, current_user_location: Location
    ) -> PaginatedResponse[AssetRead]:
        assets = self.repository.get_assets_paginated(states,asset_filter, current_user_location)
        logger.info(f"Assets read from database successfully: {assets}")
        return assets

    def read_asset(
        self, asset_id: int, current_user_location: Location
    ) -> AssetRead:
        logger.info(f"Reading asset with id: {asset_id}")

        asset_data = self.repository.get_asset_by_id(asset_id)
        if asset_data is None:
            logger.warning(f"Asset with id {asset_id} not found")
            raise NotFoundException(detail=f"Asset with id {asset_id} not found")
        if asset_data.asset_location != current_user_location:
            logger.warning(f"Asset with id {asset_id} is not in the same location as the user")
            raise BusinessException(
                detail="You can only read asset that are in the same location as you"
            )
        return asset_data 
    
    def create_asset(self, asset_data: AssetCreate, current_user: UserRead) -> AssetRead:
        
        category_service = CategoryService(self.db)
        try:
            # Log the asset creation attempt
            logger.info(f"Creating asset with name: {asset_data.asset_name}")
            category = category_service.get_category_by_id(asset_data.category_id)
            
            if not category:
                raise NotFoundException(detail="Category not found")

            # Increment the id_counter for this category
            # If id_counter is None, start from 1
            current_counter = category.id_counter
            new_counter = current_counter + 1
            category.id_counter = new_counter
            # Update the category's id_counter
            category_service.update_category(category)

            # Use the category prefix and the incremented counter
            prefix = category.prefix
            
            # Format the new asset code using the incremented counter
            asset_code = Generator.generate_asset_code(prefix, new_counter)

            # Create new asset with current timestamps
            asset_model = Asset(
                asset_code=asset_code,
                asset_name=asset_data.asset_name,
                category_id=asset_data.category_id,
                specification=asset_data.specification,
                installed_date=asset_data.installed_date,
                asset_state=asset_data.asset_state,
                asset_location=current_user.location
            )
            # Create the asset
            new_asset = self.repository.create_asset(asset_model)

            # Log the successful creation
            logger.info(f"Asset created successfully with ID: {new_asset.id}")

            return new_asset
        except Exception as e:
            # Log the error
            logger.error(f"Error creating asset: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def update_asset(self, current_user: UserRead, asset_id: int, asset_update: AssetUpdate) -> AssetRead:
        existing_asset = self.repository.get_asset_by_id(asset_id)
        if not existing_asset:
            raise NotFoundException(detail="Asset not found")
        if existing_asset.asset_location != current_user.location:
            raise BusinessException(detail="You are not allowed to update asset from other location")
        if existing_asset.asset_state == AssetState.ASSIGNED.value:
            raise BusinessException(detail="Asset is currently assigned to a user, cannot be updated")
        updated_asset = self.repository.update_asset(asset_id, asset_update)
        return updated_asset

        
    def delete_asset(self, asset_id: int, location: Location) -> None:
        """Delete asset if it has no historical assignments."""
        logger.info(f"Attempting to delete asset with id: {asset_id}")
        asset = self.read_asset(asset_id,location)

        # Note: has_historical_assignments return if the asset is valid for deletion, not whether it has historical assignments like the name suggests
        if not self.repository.has_historical_assignments(asset_id).is_valid:
            logger.warning(f"Cannot delete asset {asset_id} - has historical assignments")
            raise BusinessException(
                detail="Cannot delete the asset because it belongs to one or more historical assignments. "
                       "If the asset is not able to be used anymore, please update its state in Edit Asset page"
            )
        self.repository.delete_asset(asset)
        logger.info(f"Asset with id {asset_id} deleted successfully")
        
    def check_asset_valid(self, asset_id: int) -> IsValid:
        """Check if asset is valid for deletion."""
        asset = self.repository.get_asset_by_id(asset_id)
        
        if asset is None:
            logger.warning(f"Asset with id {asset_id} not found")
            raise NotFoundException(detail=f"Asset with id {asset_id} not found")

        return self.repository.has_historical_assignments(asset_id)
