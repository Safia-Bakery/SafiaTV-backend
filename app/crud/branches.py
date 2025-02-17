from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.Branches import Branches
from app.schemas.branches import CreateBranch, UpdateBranch


def add_branch(db: Session, data: CreateBranch):
    try:
        branch = Branches(
            name=data.name
        )
        db.add(branch)
        db.commit()
        db.refresh(branch)
        return branch

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def get_all_branches(db: Session, status):
    branches = db.query(Branches)
    if status is not None:
        branches = branches.filter(Branches.is_active == status)

    return branches.all()


def get_branch_by_id(db: Session, id):
    obj = db.query(Branches).get(ident=id)
    return obj


def edit_branch(db: Session, data: UpdateBranch):
    obj = db.query(Branches).get(ident=data.id)
    if data.name is not None:
        obj.name = data.name
    if data.is_active is not None:
        obj.is_active = data.is_active

    db.commit()
    db.refresh(obj)

    return obj

