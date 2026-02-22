"""
Delegation model
"""
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Delegation(Base):
    """Approval authority delegation"""
    __tablename__ = "delegations"

    id = Column(Integer, primary_key=True, index=True)
    delegator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    delegate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    delegator = relationship("User", foreign_keys=[delegator_id])
    delegate = relationship("User", foreign_keys=[delegate_id])
