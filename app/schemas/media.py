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


# class UpdateAccountGroup(BaseConfig):
#     id: UUID
#     name: Optional[str]
#     description: Optional[str]
#     is_active: Optional[bool]
#
#
class GetMedia(BaseConfig):
    id: UUID
    file_url: str
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    accountgroup: Optional[GetAccountGroup] = None