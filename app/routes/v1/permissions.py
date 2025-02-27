from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.permissions import get_all_permissions
from app.crud.roles import get_all_roles, get_one_role, add_role, update_role
from app.routes.depth import get_db, PermissionChecker
from app.schemas.permissions import PermissionList
from app.schemas.roles import RolesGet, CreateRole, RoleList, UpdateRole



permissions_router = APIRouter()



# @permissions_router.get('/permission_pages', response_model=List[PermissionList])
# async def get_role_list(
#         page_id: Optional[UUID] = None,
#         db: Session = Depends(get_db),
#         # current_user: dict = Depends(PermissionChecker(required_permissions='view_role'))
# ):
#     permissions = get_all_permissions(db=db, page_id=page_id)
#     return permissions



@permissions_router.get('/permissions', response_model=List[PermissionList])
async def get_permission_list(
        page_id: Optional[UUID] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='view_permission'))
):
    permissions = get_all_permissions(db=db, page_id=page_id)
    return permissions
