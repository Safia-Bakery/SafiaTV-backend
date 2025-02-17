from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.roles import get_all_roles, get_one_role, add_role, update_role
from app.routes.depth import get_db, PermissionChecker
from app.schemas.roles import RolesGet, CreateRole, RoleList, UpdateRole



roles_router = APIRouter()



@roles_router.get('/roles', response_model=List[RoleList])
async def get_role_list(
        status: Optional[bool] = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_role'))
):
    roles = get_all_roles(db=db)
    return roles


@roles_router.get('/roles/{id}', response_model=RolesGet)
async def get_role(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_role'))
):
    role = get_one_role(db=db, role_id=id)
    return role


@roles_router.post('/roles', response_model=RolesGet)
async def create_roles(
        body: CreateRole,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='create_role'))
):
    created_role = add_role(db=db, data=body)
    return created_role


@roles_router.put('/roles', response_model=RolesGet)
async def update_roles(
        body: UpdateRole,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='edit_role'))
):
    updated_role = update_role(db=db, data=body)
    return updated_role

