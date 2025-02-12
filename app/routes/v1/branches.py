from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.branches import add_branch, get_all_branches, get_branch_by_id, edit_branch
from app.routes.depth import get_db, PermissionChecker
from app.schemas.branches import CreateBranch, GetBranch, UpdateBranch


branches_router = APIRouter()


@branches_router.post("/branches", response_model=GetBranch)
async def create_branch(
        data: CreateBranch,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='create_branch'))
):
    created_branch = add_branch(db=db, data=data)
    return created_branch


@branches_router.get("/branches", response_model=Page[GetBranch])
async def get_branch_list(
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_branch'))
):
    branches = get_all_branches(db=db)
    return paginate(branches)


@branches_router.get("/branches/{id}", response_model=GetBranch)
async def get_branch(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_branch'))
):
    branch = get_branch_by_id(db=db, id=id)
    return branch


@branches_router.put("/branches", response_model=GetBranch)
async def update_branch(
        data: UpdateBranch,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='edit_branch'))
):
    branch = edit_branch(db=db, data=data)
    return branch

