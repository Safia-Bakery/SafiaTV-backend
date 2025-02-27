from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.branch_account_groups import get_branch_account_groups
from app.crud.branches import add_branch, get_all_branches, get_branch_by_id, edit_branch, remove_branch
from app.routes.depth import get_db, PermissionChecker
from app.schemas.branch_account_groups import GetBranchAccountGroups
from app.schemas.branches import CreateBranch, GetBranch, UpdateBranch


branches_router = APIRouter()


@branches_router.post("/branches", response_model=GetBranch)
async def create_branch(
        data: CreateBranch,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='create_branch'))
):
    created_branch = add_branch(db=db, data=data)
    return created_branch


@branches_router.get("/branches", response_model=Page[GetBranch])
async def get_branch_list(
        name: Optional[str] = None,
        status: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='view_branch'))
):
    branches = get_all_branches(db=db, status=status, name=name)
    return paginate(branches)


@branches_router.get("/branches/{id}", response_model=GetBranchAccountGroups)
async def get_branch(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='view_branch'))
):
    branch = get_branch_account_groups(db=db, branch_id=id)
    return branch


@branches_router.put("/branches", response_model=GetBranch)
async def update_branch(
        data: UpdateBranch,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='edit_branch'))
):
    branch = edit_branch(db=db, data=data)
    return branch


@branches_router.delete("/branches")
async def delete_branch(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='delete_branch'))
):
    branch = remove_branch(db=db, id=id)
    return {"Status": f"Branch {branch.name} was deleted successfully"}
