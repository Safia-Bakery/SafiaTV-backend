from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class GetBranch(BaseConfig):
    id: UUID
    name: str
