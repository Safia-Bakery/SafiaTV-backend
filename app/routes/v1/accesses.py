from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.roles import create_accesses, delete_accesses
from app.routes.depth import get_db, PermissionChecker
from app.schemas.roles import AccessesGet, CreateAccess



accesses_router = APIRouter()



@accesses_router.post('/accesses', response_model=AccessesGet)
async def create_access(
        body: CreateAccess,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='create_access'))
):
    created_access = create_accesses(db=db, role_id=body.role_id, permission_id=body.permission_id)
    return created_access



@accesses_router.delete('/accesses')
async def delete_access(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='delete_access'))
):
    delete_accesses(db=db, id=id)
    return {"Result": "Item deleted successfully"}

