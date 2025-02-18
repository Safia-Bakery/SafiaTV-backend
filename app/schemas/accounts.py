from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.account_groups import GetAccountGroup
from app.schemas.branches import GetBranch
from app.schemas.roles import RolesGet



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )



class GetAccountFullData(BaseConfig):
    id: Optional[UUID] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[RolesGet] = None
    accountgroup: Optional[GetAccountGroup] = None
    branch: Optional[GetBranch] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class GetAccounts(BaseConfig):
    id: Optional[UUID] = None
    is_active: Optional[bool] = None
    accountgroup: Optional[GetAccountGroup] = None



class AccountLogin(BaseConfig):
    password: str



class CreateAccount(BaseConfig):
    password: str
    role_id: UUID
    accountgroup_id: Optional[UUID] = None
    branch_id: Optional[UUID] = None



class UpdateAccount(BaseConfig):
    id: UUID
    password: Optional[str] = None
    is_active: Optional[bool] = True
    role_id: Optional[UUID] = None
    accountgroup_id: Optional[UUID] = None
    branch_id: Optional[UUID] = None
