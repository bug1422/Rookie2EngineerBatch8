from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.asset import AssetCreate, AssetRead, AssetUpdate
from schemas.query.check.isValid import IsValid
from services.asset import AssetService
from api.dependencies import get_db_session, get_current_admin
from schemas.shared.paginated_response import PaginatedResponse
from schemas.query.filter.asset import AssetFilter
from schemas.user import UserRead
from schemas.query.filter.assignment import AssignmentFilter
from services.assignment import AssignmentService
from schemas.asset import AssetHistory
from enums.asset.state import AssetState
from typing import Optional

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("", 
            response_model=PaginatedResponse[AssetRead],
            status_code=status.HTTP_200_OK,
            summary="Get paginated list of assets",
            description="Get a paginated list of assets with optional filters.")
async def get_assets(
    states: Optional[list[AssetState]] = Query(None, description="Filter by asset state", alias="states[]"),
    filter: AssetFilter = Depends(), 
    db: Session = Depends(get_db_session), 
    current_user = Depends(get_current_admin)
):
    asset_service = AssetService(db)
    return asset_service.read_assets_paginated(states,filter, current_user.location)


@router.get(
    "/{asset_id}/history",
    response_model=PaginatedResponse[AssetHistory],
    status_code=status.HTTP_200_OK,
    summary="Get asset history by asset ID",
    description="Get a paginated list of asset history by asset ID.",
)
async def get_asset_history(
    asset_id: int,
    filter: AssignmentFilter = Depends(),
    db: Session = Depends(get_db_session),
    current_user=Depends(get_current_admin),
):
    assignment_service = AssignmentService(db)
    return assignment_service.get_assignment_history(asset_id, filter, current_user)

@router.get("/{asset_id}", 
            response_model=AssetRead,
            status_code=status.HTTP_200_OK,
            summary="Get asset by ID",
            description="Get an asset full details by its ID.")
async def get_asset_by_id(
    asset_id: int, 
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_admin)
):
    asset_service = AssetService(db)
    return asset_service.read_asset(asset_id,current_user.location)

@router.post("", 
             response_model=AssetRead,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new asset",
             description="Create a new asset with the provided details.")
async def create_asset(asset: AssetCreate, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_admin)):
    service = AssetService(db)
    try:
        return service.create_asset(asset, current_user)
    except HTTPException as e:
        raise e

@router.put("/{asset_id}", 
            response_model=AssetRead,
            status_code=status.HTTP_200_OK,
            summary="Update asset by ID",
            description="Update an asset by its ID with the provided details.")
async def update_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_admin)):
    return AssetService(db).update_asset(current_user, asset_id, asset)

@router.delete("/{asset_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete asset by ID",
               description="Delete an asset by its ID. Only assets with no historical assignments can be deleted.")
async def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_admin)
):
    current_location = current_user.location
    asset_service = AssetService(db)
    asset_service.delete_asset(asset_id, current_location)
    
@router.get(
    "/valid-asset/{asset_id}",
    response_model=IsValid,
    status_code=status.HTTP_200_OK,
    summary="Get and check if asset is valid by ID",
    description="Get an asset and check if asset is valid by ID. Asset is valid if it has no historical assignments.",
)
async def get_valid_asset(asset_id: int, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_admin)):
    """Get a valid user by ID"""
    asset_service = AssetService(db)
    return asset_service.check_asset_valid(asset_id)
