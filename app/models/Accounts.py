import uuid
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime, BIGINT, Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base



class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    password = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete="SET NULL"))
    role = relationship('Roles', back_populates='accounts')
    accountgroup_id = Column(UUID(as_uuid=True), ForeignKey('account_groups.id', ondelete="SET NULL"))
    accountgroup = relationship('AccountGroups', back_populates='accounts')
    branch_id = Column(UUID(as_uuid=True), ForeignKey('branches.id', ondelete="CASCADE"))
    branch = relationship('Branches', back_populates='accounts')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
