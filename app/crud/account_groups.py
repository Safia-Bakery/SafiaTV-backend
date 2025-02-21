from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.AccountGroups import AccountGroups
from app.schemas.account_groups import CreateAccountGroup, UpdateAccountGroup


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


def get_account_groups(db: Session, status):
    objs = db.query(AccountGroups)
    if status is not None:
        objs = objs.filter(AccountGroups.is_active == status)

    return objs.all()


def get_one_account_group(db: Session, group_id):
    obj = db.query(AccountGroups).get(ident=group_id)
    return obj


def edit_account_group(db: Session, data: UpdateAccountGroup):
    obj = db.query(AccountGroups).get(ident=data.id)
    if data.name is not None:
        obj.name = data.name
    if data.description is not None:
        obj.description = data.description
    if data.is_active is not None:
        obj.is_active = data.is_active

    db.commit()
    db.refresh(obj)
    return obj



def remove_account_group(db: Session, group_id):
    obj = db.query(AccountGroups).get(ident=group_id)
    db.delete(obj)
    db.commit()
    return obj

