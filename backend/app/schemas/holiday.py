"""
Holiday schemas
"""
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class HolidayCreate(BaseModel):
    """Schema for creating a holiday"""
    name: str
    date: date
    is_mandatory: bool = True


class HolidayUpdate(BaseModel):
    """Schema for updating a holiday"""
    name: Optional[str] = None
    date: Optional[date] = None
    is_mandatory: Optional[bool] = None


class HolidayResponse(BaseModel):
    """Schema for holiday response"""
    id: int
    name: str
    date: date
    is_mandatory: bool
    created_by: int

    model_config = ConfigDict(from_attributes=True)
