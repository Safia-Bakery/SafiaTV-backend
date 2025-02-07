from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.account_groups import GetAccountGroup
from app.schemas.roles import RolesGet



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )



class GetAccountFullData(BaseConfig):
    id: Optional[UUID] = None
    password: Optional[str] = None
    role: Optional[RolesGet] = None
    accountgroup: Optional[GetAccountGroup] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class GetAccount(BaseConfig):
    id: Optional[UUID] = None
    password: Optional[str] = None



class AccountLogin(BaseConfig):
    password: str



class CreateAccount(BaseConfig):
    password: str
    role_id: UUID
    accountgroup_id: Optional[UUID] = None

