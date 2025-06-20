from enum import Enum

class AssetState(str, Enum):
    AVAILABLE = "Available"
    NOT_AVAILABLE = "Not Available"
    ASSIGNED = "Assigned"
    WAITING_FOR_RECYCLING = "Waiting for Recycling"
    RECYCLED = "Recycled"
