import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime, Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base



class AccountGroups(Base):
    __tablename__ = "account_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    accounts = relationship('Accounts', back_populates='accountgroup', passive_deletes=True)
    branches = relationship('AccountGroupBranchRelations', back_populates='accountgroup', cascade="all, delete")
    media = relationship('Media', back_populates='accountgroup', passive_deletes=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
