import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean, ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Media(Base):
    __tablename__ = 'media'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    file_url = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    accountgroup_id = Column(UUID(as_uuid=True), ForeignKey('account_groups.id'))
    accountgroup = relationship('AccountGroups', back_populates='media')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
