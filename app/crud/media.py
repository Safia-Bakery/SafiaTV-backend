from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.media import CreateMedia
from app.models.Media import Media



def add_media(db: Session, data: CreateMedia):
    try:
        role = Media(
            name=data.name,
            file_url=data.file_url,
            description=data.description,
            accountgroup_id=data.accountgroup_id
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def get_all_medias(db: Session):
    medias = db.query(Media).all()
    return medias