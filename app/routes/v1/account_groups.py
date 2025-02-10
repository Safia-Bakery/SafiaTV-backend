from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.account_groups import add_account_group, get_account_groups, get_one_account_group, edit_account_group
from app.routes.depth import get_db
from app.schemas.account_groups import CreateAccountGroup, GetAccountGroup, UpdateAccountGroup

account_group_router = APIRouter()



@account_group_router.get('/accounts-groups', response_model=List[GetAccountGroup])
async def get_account_group_list(
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_role'))
):
    account_groups = get_account_groups(db=db)
    return account_groups


@account_group_router.get('/accounts-groups/{id}', response_model=GetAccountGroup)
async def get_account_group(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_role'))
):
    account_group = get_one_account_group(db=db, group_id=id)
    return account_group


@account_group_router.post('/accounts-groups', response_model=GetAccountGroup)
async def create_account_groups(
        data: CreateAccountGroup,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='create_role'))
):
    created_account_group = add_account_group(db=db, data=data)
    return created_account_group


@account_group_router.put('/accounts-groups', response_model=GetAccountGroup)
async def update_account_group(
        data: UpdateAccountGroup,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='edit_role'))
):
    updated_obj = edit_account_group(db=db, data=data)
    return updated_obj

