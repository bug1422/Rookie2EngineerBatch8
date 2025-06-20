from enum import Enum

class SortDirection(str, Enum):
    """Enum for sorting direction."""
    ASC = "asc"
    DESC = "desc"
    
class SortUserBy(str, Enum):
    """Enum for sort user by."""
    STAFF_CODE = "staff_code"
    FIRST_NAME = "first_name"
    JOIN_DATE = "join_date"
    TYPE = "type"
    UPDATED_AT = "updated_at"
    
class SortAssignmentBy(str, Enum):
    """Enum for sort assignment by."""
    ID = "id"
    ASSET_CODE = "asset_code"
    ASSET_NAME = "asset_name"
    ASSIGNED_TO = "assigned_to"
    ASSIGNED_BY = "assigned_by"
    ASSIGN_DATE = "assign_date"
    STATE = "state"
    UPDATED_AT = "updated_at"
    
class SortRequestBy(str, Enum):
    """Enum for sort request by."""
    ID = "id"
    ASSET_CODE = "asset_code"
    ASSET_NAME = "asset_name"
    REQUESTED_BY = "requested_by"
    ASSIGN_DATE = "assign_date"
    ACCEPTED_BY = "accepted_by"
    RETURN_DATE = "return_date"
    STATE = "state"
    
class SortAssetBy(str, Enum):
    """Enum for sort asset by."""
    ASSET_CODE = "asset_code"
    ASSET_NAME = "asset_name"
    CATEGORY = "category"
    STATE = "state"
    UPDATED_AT = "updated_at"
    
class SortReportBy(str, Enum):
    """Enum for sort report by."""
    CATEGORY = "category"
    TOTAL = "total"
    ASSIGNED = "assigned"
    AVAILABLE = "available"
    NOT_AVAILABLE = "not_available"
    WAITING_FOR_RECYCLING = "waiting_for_recycling"
    RECYCLED = "recycled"

class SortHomeAssignmentBy(str, Enum):
    """Enum for sort home assignment by."""
    ASSET_CODE = "asset_code"
    ASSET_NAME = "asset_name"
    CATEGORY = "category"
    STATE = "state"
    ASSIGN_DATE = "assign_date"
