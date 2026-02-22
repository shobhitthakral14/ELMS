"""
Holiday model
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Holiday(Base):
    """Company holidays"""
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User")
