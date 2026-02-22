"""
Delegation schemas
"""
from pydantic import BaseModel, ConfigDict
from datetime import date


class DelegationCreate(BaseModel):
    """Schema for creating a delegation"""
    delegate_id: int
    start_date: date
    end_date: date


class DelegationResponse(BaseModel):
    """Schema for delegation response"""
    id: int
    delegator_id: int
    delegator_name: str
    delegate_id: int
    delegate_name: str
    start_date: date
    end_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
