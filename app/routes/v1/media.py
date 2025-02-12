from uuid import UUID

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.media import add_media, get_all_medias, get_device_medias, edit_media
from app.routes.depth import get_db, get_current_user, PermissionChecker
from app.schemas.media import CreateMedia, GetMedia, UpdateMedia

media_router = APIRouter()


@media_router.post("/media", response_model=GetMedia)
async def create_media(
    data: CreateMedia,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(PermissionChecker(required_permissions='create_media'))
):
    created_media = add_media(db=db, data=data)
    return created_media


@media_router.get("/media", response_model=Page[GetMedia])
async def get_media_list(
    db: Session = Depends(get_db),
    # current_user: dict = Depends(PermissionChecker(required_permissions='view_media'))
):
    medias = get_all_medias(db=db)
    return paginate(medias)



@media_router.get("/media/device", response_model=Page[GetMedia])
async def get_media_list(
    account_group: UUID,
    branch_id: UUID,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(PermissionChecker(required_permissions='view_media'))
):
    medias = get_device_medias(db=db, branch_id=branch_id, account_group=account_group)
    # medias = get_device_medias(db=db, branch_id=current_user.branch_id, account_group=current_user.account_group)
    return paginate(medias)



@media_router.put("/media", response_model=GetMedia)
async def update_media(
        data: UpdateMedia,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='edit_media'))
):
    media = edit_media(db=db, data=data)
    return media

