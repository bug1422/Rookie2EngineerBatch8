from schemas.query.check.isValid import IsValid
from schemas.shared.paginated_response import PaginatedResponse, PaginationMeta
from schemas.query.filter.asset import AssetFilter
from schemas.query.sort.sort_type import SortAssetBy, SortDirection
from schemas.asset import AssetRead, AssetUpdate
from models.asset import Asset
from models.assignment import Assignment
from models.category import Category
from sqlmodel import Session, func
from enums.shared.location import Location
from enums.asset.state import AssetState
from datetime import datetime, timezone
from typing import List, Optional


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_assets_paginated(
        self, states: Optional[List[AssetState]], asset_filter: AssetFilter, current_user_location: Location
    ) -> PaginatedResponse[AssetRead]:
        query = self.db.query(Asset)\
            .join(Category, onclause=Asset.category_id == Category.id,
                  isouter=True)
        query = query.filter(Asset.asset_location == current_user_location)        
        print(states)
        if states:
            query = query.filter(Asset.asset_state.in_(states))

        if asset_filter.category:
            query = query.filter(
                Category.category_name.ilike(f"%{asset_filter.category}%"))

        if asset_filter.search:
            query = query.filter(
                (Asset.asset_code.ilike(f"%{asset_filter.search}%"))
                | (Asset.asset_name.ilike(f"%{asset_filter.search}%"))
            )

        if asset_filter.sort_by:
            if asset_filter.sort_by == SortAssetBy.ASSET_CODE:
                query = query.order_by(
                    Asset.asset_code.asc()
                    if asset_filter.sort_direction == SortDirection.ASC
                    else Asset.asset_code.desc()
                )
            elif asset_filter.sort_by == SortAssetBy.ASSET_NAME:
                query = query.order_by(
                    func.lower(Asset.asset_name).asc()
                    if asset_filter.sort_direction == SortDirection.ASC
                    else func.lower(Asset.asset_name).desc()
                )
            elif asset_filter.sort_by == SortAssetBy.CATEGORY:
                query = query.order_by(
                    func.lower(Category.category_name).asc()
                    if asset_filter.sort_direction == SortDirection.ASC
                    else func.lower(Category.category_name).desc()
                )
            elif asset_filter.sort_by == SortAssetBy.STATE:
                query = query.order_by(
                    Asset.asset_state.asc()
                    if asset_filter.sort_direction == SortDirection.ASC
                    else Asset.asset_state.desc()
                )
            elif asset_filter.sort_by == SortAssetBy.UPDATED_AT:
                query = query.order_by(
                    Asset.updated_at.asc()
                    if asset_filter.sort_direction == SortDirection.ASC
                    else Asset.updated_at.desc()
                )

        total = query.count()
        total_pages = (total + asset_filter.size - 1) // asset_filter.size

        assets = (
            query.offset((asset_filter.page - 1) * asset_filter.size)
            .limit(asset_filter.size)
            .all()
        )

        return PaginatedResponse(
            data=assets,
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=asset_filter.page,
                page_size=asset_filter.size,
            ),
        )

    def get_asset_by_id(self, asset_id: int) -> Asset:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def create_asset(self, asset_data: Asset) -> Asset:
        """Create a new asset."""
        # Retrieve the category to get the prefix

        self.db.add(asset_data)
        self.db.commit()
        self.db.refresh(asset_data)
        return asset_data

    def update_asset(self, asset_id: int, asset_update: AssetUpdate) -> Asset:
        """Update an asset."""
        asset = self.db.query(Asset).filter(Asset.id == asset_id).first()

        # Get only the set fields from update request
        update_data = asset_update.model_dump(exclude_unset=True)

        # Update only the fields that were provided
        for field, value in update_data.items():
            if hasattr(asset, field):
                setattr(asset, field, value)

        asset.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete_asset(self, asset: Asset) -> None:
        self.db.delete(asset)
        self.db.commit()

    def has_historical_assignments(self, asset_id: int) -> IsValid:
        if self.db.query(Assignment).filter(Assignment.asset_id == asset_id).count() > 0:
            return IsValid(is_valid=False, detail="Asset has historical assignments")
        return IsValid(is_valid=True, detail="Asset has no historical assignments")
