from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.branch_account_groups import add_branch_group, delete_record
from app.routes.depth import get_db, PermissionChecker
from app.schemas.branch_account_groups import CreateBranchAccountGroups


branch_account_group_router = APIRouter()


@branch_account_group_router.post("/branch-account-groups")
async def create_branch_account_group(
        data: CreateBranchAccountGroups,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='create_account_group_branch_relation'))
):
    # branch_account_groups = []
    for account_group in data.account_groups:
        # created_branch_group = add_branch_group(db=db, branch_id=data.branch_id, account_group=account_group)
        add_branch_group(db=db, branch_id=data.branch_id, account_group=account_group)
        # branch_account_groups.append(created_branch_group)

    return {"Items created successfully"}



# @branch_account_group_router.get("/branch-account-groups", response_model=GetBranchAccountGroups)
# async def get_branch_account_group_list(
#         branch_id: UUID,
#         db: Session = Depends(get_db),
#         # current_user: dict = Depends(PermissionChecker(required_permissions='view_account_group_branch_relation'))
# ):
#     objs = get_branch_account_groups(db=db, branch_id=branch_id)
#     return objs


@branch_account_group_router.delete("/branch-account-groups/{id}")
async def delete_branch_account_group(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='delete_account_group_branch_relation'))
):
    removed_obj = delete_record(db=db, id=id)
    if removed_obj is None:
        raise HTTPException(status_code=404, detail="The item was not found !")

    return  {"Message": "Item deleted successfully"}