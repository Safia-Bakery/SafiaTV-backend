import uuid

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime, Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Branches(Base):
    __tablename__ = "branches"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    accountgroups = relationship("AccountGroupBranchRelations", back_populates="branch", cascade="all, delete")
    accounts = relationship("Accounts", back_populates="branch", cascade="all, delete")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
