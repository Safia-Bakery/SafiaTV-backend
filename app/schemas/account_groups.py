from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.branches import GetBranch


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class CreateAccountGroup(BaseConfig):
    name: str
    description: Optional[str]


class UpdateAccountGroup(BaseConfig):
    id: UUID
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]


class GetAccountGroup(BaseConfig):
    id: UUID
    name: str
    description: Optional[str]
    is_active: Optional[bool]
    # accounts: Optional[List[GetAccount]] = None
    # branches: Optional[List[GetBranch]] = None

