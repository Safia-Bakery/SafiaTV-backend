import os
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.media import add_media, get_all_medias, get_device_medias, edit_media, remove_media
from app.routes.depth import get_db, get_current_user, PermissionChecker
from app.schemas.media import CreateMedia, GetMedia, UpdateMedia
from app.utils.websocket_connection import manager



media_router = APIRouter()



@media_router.post("/media", response_model=GetMedia)
async def create_media(
    data: CreateMedia,
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions='create_media'))
):
    created_media = add_media(db=db, data=data)
    try:
        await manager.broadcast(data="Был добавлен контент")
    except Exception as e:
        print(f"Ошибка с отправкой инфо: {e}")

    return created_media



@media_router.get("/media", response_model=Page[GetMedia])
async def get_media_list(
    id: Optional[UUID] = None,
    status: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions='view_media'))
):
    medias = get_all_medias(db=db, media_id=id, status=status)
    return paginate(medias)



@media_router.get("/media/device", response_model=Page[GetMedia])
async def get_device_media(
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions='view_media'))
):
    medias = get_device_medias(db=db, branch_id=current_user["branch_id"], account_group=current_user["account_group"])
    return paginate(medias)



@media_router.put("/media", response_model=GetMedia)
async def update_media(
        data: UpdateMedia,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='edit_media'))
):
    media = edit_media(db=db, data=data)
    try:
        await manager.broadcast(data="Был обновлен контент")
    except Exception as e:
        print(f"Ошибка с отправкой инфо: {e}")

    return media


@media_router.delete('/media')
async def delete_media(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions='delete_media'))
):
    media = remove_media(db=db, id=id)
    # print("DELETED MEDIA: ", media)
    file_path = media.file_url
    # print("file_path: ", file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        # print(f"{file_path} deleted successfully.")
    else:
        print(f"{file_path} not found.")

    try:
        await manager.broadcast(data="Был удален контент")
    except Exception as e:
        print(f"Ошибка с отправкой инфо: {e}")

    return {"Status": f"Media {media.name} was deleted successfully"}

