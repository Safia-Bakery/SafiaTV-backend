import uuid

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class AccountGroupBranchRelations(Base):
    __tablename__ = "accountgroup_branch_relations"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    accountgroup_id = Column(UUID(as_uuid=True), ForeignKey('account_groups.id', ondelete="CASCADE"))
    accountgroup = relationship("AccountGroups", back_populates="branches")
    branch_id = Column(UUID(as_uuid=True), ForeignKey('branches.id', ondelete="CASCADE"))
    branch = relationship("Branches", back_populates="accountgroups")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
