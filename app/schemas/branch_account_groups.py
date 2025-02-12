from typing import Optional, List
from uuid import UUID
from app.schemas.account_groups import GetAccountGroup
from app.schemas.branches import GetBranch
from app.schemas.accounts import GetAccount
from pydantic import BaseModel, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class GetBranchAccountGroups(BaseConfig):
    branch: Optional[GetBranch]
    accounts: Optional[List[GetAccount]]
    account_groups: Optional[List[GetAccountGroup]]


class CreateBranchAccountGroups(BaseConfig):
    branch_id: UUID
    account_groups: List[UUID]

