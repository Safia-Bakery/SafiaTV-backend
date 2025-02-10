from typing import Optional, List
from uuid import UUID
from app.schemas.account_groups import GetAccountGroup
from app.schemas.branches import GetBranch
from pydantic import BaseModel, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class GetBranchAccountGroups(BaseConfig):
    branch: Optional[GetBranch]
    account_groups: Optional[List[GetAccountGroup]]


class CreateBranchAccountGroups(BaseConfig):
    branch_id: UUID
    account_groups: List[UUID]

