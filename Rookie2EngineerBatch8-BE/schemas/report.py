from pydantic import BaseModel

class ReportRead(BaseModel):
    """Report model"""
    category: str
    total: int = 0
    assigned: int = 0
    available: int = 0
    not_available: int = 0
    waiting_for_recycling: int = 0
    recycled: int = 0
