from typing import Optional
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.Branches import Branches
from app.models.AccountGroups import AccountGroups
from app.crud.branches import get_branch_by_id
from app.models.AccountGroupBranchRelations import AccountGroupBranchRelations



def add_branch_group(db: Session, branch_id, account_group):
    try:
        obj = AccountGroupBranchRelations(
            accountgroup_id=account_group,
            branch_id=branch_id
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def get_branch_account_groups(db: Session, branch_id):
    branch = get_branch_by_id(db=db, id=branch_id)
    account_groups = db.query(
        AccountGroups
    ).join(
        AccountGroupBranchRelations, AccountGroups.id == AccountGroupBranchRelations.accountgroup_id
    ).filter(
        AccountGroupBranchRelations.branch_id == branch_id
    ).all()

    data_dict = {
        "branch": branch,
        "accounts": branch.accounts,
        "account_groups": account_groups
    }
    return data_dict


def delete_record(db: Session, id):
    obj = db.query(AccountGroupBranchRelations).get(ident=id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

