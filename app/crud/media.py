from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.media import CreateMedia, UpdateMedia
from app.models.Media import Media
from app.models.AccountGroupBranchRelations import AccountGroupBranchRelations



def add_media(db: Session, data: CreateMedia):
    try:
        media = Media(
            name=data.name,
            file_url=data.file_url,
            description=data.description,
            accountgroup_id=data.accountgroup_id
        )
        db.add(media)
        db.commit()
        db.refresh(media)
        return media

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def get_all_medias(db: Session, media_id, status):
    medias = db.query(Media)
    if media_id is not None:
        medias = medias.filter(Media.id == media_id)
        return medias.all()
    if status is not None:
        medias = medias.filter(Media.is_active == status)

    return medias.all()


def get_media(db: Session, id):
    media = db.query(Media).get(ident=id)
    return media


def get_device_medias(db: Session, branch_id, account_group):
    branch_account_group = db.query(
        AccountGroupBranchRelations.accountgroup_id
    ).filter(
        and_(
            AccountGroupBranchRelations.branch_id == branch_id,
            AccountGroupBranchRelations.accountgroup_id == account_group
        )
    )
    medias = db.query(
        Media
    ).filter(
        and_(
            Media.is_active == True,
            Media.accountgroup_id == branch_account_group
        )
    ).all()

    return medias



def edit_media(db: Session, data: UpdateMedia):
    obj = db.query(Media).get(ident=data.id)
    if data.file_url is not None:
        obj.file_url = data.file_url
    if data.name is not None:
        obj.name = data.name
    if data.description is not None:
        obj.description = data.description
    if data.accountgroup_id is not None:
        obj.accountgroup_id = data.accountgroup_id
    if data.is_active is not None:
        obj.is_active = data.is_active

    db.commit()
    db.refresh(obj)

    return obj
