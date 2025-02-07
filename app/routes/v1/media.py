from uuid import UUID

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.media import add_media, get_all_medias
from app.routes.depth import get_db, get_current_user
from app.schemas.media import CreateMedia, GetMedia

# from app.schemas.users import GetUserFullData
# from app.utils.utils import generate_random_string


media_router = APIRouter()


@media_router.post("/media", response_model=GetMedia)
async def create_media(
    data: CreateMedia,
    db: Session = Depends(get_db),
    # current_user: GetUserFullData = Depends(get_current_user),
):
    created_media = add_media(db=db, data=data)
    return created_media


@media_router.get("/media", response_model=Page[GetMedia])
async def get_media_list(
    db: Session = Depends(get_db),
    # current_user: GetUserFullData = Depends(get_current_user),
):
    medias = get_all_medias(db=db)
    return paginate(medias)



# @media_router.get("/media/{account_group}", response_model=Page[GetMedia])
@media_router.get("/media/device")
async def get_media_list(
    # account_group: UUID,
    db: Session = Depends(get_db),
    # current_user: GetUserFullData = Depends(get_current_user),
):
    # medias = get_all_medias(db=db)
    # return paginate(medias)
    return []