from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.Accounts import Accounts
from app.models.Roles import Roles
from app.models.Accesses import Accesses
from app.models.Permissions import Permissions
from app.schemas.accounts import UpdateAccount
from app.utils.utils import hash_password



def create_account(
        db:Session,
        password,
        role_id,
        accountgroup_id: Optional[UUID] = None,
        branch_id: Optional[UUID] = None
):
    try:
        query = Accounts(
            password=password,
            role_id=role_id,
            accountgroup_id=accountgroup_id,
            branch_id=branch_id
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query
    except IntegrityError as e:
        db.rollback()
        print(e)
        return None



def get_account_by_username(db:Session, username):
    query = db.query(Accounts).filter(
        and_(
            Accounts.is_active.is_(True),
            Accounts.username == username
        )
    ).first()
    return query



def get_account_by_password(db:Session, password):
    query = db.query(Accounts).filter(
        and_(
            Accounts.is_active.is_(True),
            Accounts.password == password
        )
    ).first()
    # if query:
    #     accesses = db.query(Accesses).filter(Accesses.role_id == query.role_id).all()
    #     permissions = []
    #     for access in accesses:
    #         permissions.append(access.permission_id)
    #
    #     query.role.permissions = permissions

    return query


def get_account_list(db:Session):
    query = db.query(Accounts).all()
    return  query



def get_account_by_id(db:Session, id):
    query = db.query(Accounts).get(ident=id)
    return query


def edit_account(db:Session, data: UpdateAccount):
    query = db.query(Accounts).get(ident=data.id)
    if data.password is not None:
        query.password = data.password
    if data.is_active is not None:
        query.is_active = data.is_active
    if data.role_id is not None:
        query.role_id = data.role_id
    if data.accountgroup_id is not None:
        query.accountgroup_id = data.accountgroup_id
    if data.branch_id is not None:
        query.branch_id = data.branch_id

    db.commit()
    db.refresh(query)

    return query



def remove_account(db:Session, id):
    query = db.query(Accounts).get(ident=id)
    db.delete(query)
    db.commit()
    return query
