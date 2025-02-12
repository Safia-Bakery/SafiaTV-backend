from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.account_groups import GetAccountGroup


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class CreateMedia(BaseConfig):
    name: Optional[str] = None
    file_url: Optional[str]
    description: Optional[str] = None
    accountgroup_id: Optional[UUID] = None


class UpdateMedia(BaseConfig):
    id: UUID
    name: Optional[str] = None
    file_url: Optional[str] = None
    description: Optional[str] = None
    accountgroup_id: Optional[UUID] = None
    is_active: Optional[bool] = None



class GetMedia(BaseConfig):
    id: UUID
    file_url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    accountgroup: Optional[GetAccountGroup] = None
