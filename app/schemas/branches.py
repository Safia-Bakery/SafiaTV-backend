from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class GetBranch(BaseConfig):
    id: UUID
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CreateBranch(BaseConfig):
    name: str


class UpdateBranch(BaseConfig):
    id: UUID
    name: Optional[str] = None
    is_active: Optional[bool] = None
