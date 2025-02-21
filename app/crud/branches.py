from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import AccountGroupBranchRelations
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


def get_all_branches(db: Session, status, name):
    branches = db.query(Branches)
    if status is not None:
        branches = branches.filter(Branches.is_active == status)
    if name is not None:
        branches = branches.filter(Branches.name.ilike(f"%{name}%"))

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
    if data.account_groups is not None:
        relations = db.query(AccountGroupBranchRelations).filter(AccountGroupBranchRelations.branch_id == data.id).all()
        account_groups = [relation.accountgroup_id for relation in relations]
        for group in account_groups:
            if group not in data.account_groups:
                access = db.query(AccountGroupBranchRelations).filter(
                    and_(
                        AccountGroupBranchRelations.branch_id == data.id,
                        AccountGroupBranchRelations.accountgroup_id == group
                    )
                ).first()
                db.delete(access)
                db.flush()

        for group in data.account_groups:
            if group not in account_groups:
                access = AccountGroupBranchRelations(
                    accountgroup_id=group,
                    branch_id=obj.id
                )
                db.add(access)
                db.flush()

    db.commit()
    db.refresh(obj)

    return obj



def remove_branch(db: Session, id):
    obj = db.query(Branches).get(ident=id)
    db.delete(obj)
    db.commit()
    return obj
