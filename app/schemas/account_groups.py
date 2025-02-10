from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class CreateAccountGroup(BaseConfig):
    name: str
    description: Optional[str]


class UpdateAccountGroup(BaseConfig):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class GetAccountGroup(BaseConfig):
    id: UUID
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = None

