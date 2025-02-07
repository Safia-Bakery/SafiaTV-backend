from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.AccountGroups import AccountGroups
from app.schemas.account_groups import CreateAccountGroup


def add_account_group(db:Session, data: CreateAccountGroup):
    try:
        obj = AccountGroups(
            name=data.name,
            description=data.description
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def get_account_groups(db: Session):
    objs = db.query(AccountGroups).all()
    return objs


def get_one_account_group(db: Session, group_id):
    obj = db.query(AccountGroups).get(ident=group_id)
    return obj
