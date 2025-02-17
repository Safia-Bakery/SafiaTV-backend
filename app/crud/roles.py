from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.Accesses import Accesses
from app.models.Roles import Roles
from app.schemas.roles import CreateRole, UpdateRole


def create_role(db:Session, name, description):
    query = Roles(
        name=name,
        description=description,
        is_active=True
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return  query



def get_role_by_name(db:Session,name):
    query = db.query(Roles).filter(Roles.name==name).first()
    return query





def create_accesses(db:Session,role_id,permission_id):
    query = Accesses(role_id=role_id,permission_id=permission_id)
    db.add(query)
    db.commit()
    return query



def delete_accesses(db: Session, id):
    obj = db.query(Accesses).get(ident=id)
    db.delete(obj)
    db.commit()



def get_all_roles(db: Session, status):
    query = db.query(Roles)
    if status is not None:
        query = query.filter(Roles.is_active == status)

    return query.all()


def get_one_role(db: Session, role_id):
    query = db.query(Roles).get(ident=role_id)
    return query


def add_role(db:Session, data: CreateRole):
    try:
        role = Roles(
            name=data.name,
            description=data.description,
            is_active=data.is_active
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def update_role(db:Session, data: UpdateRole):
    role = db.query(Roles).get(ident=data.id)
    if data.name is not None:
        role.name = data.name
    if data.description is not None:
        role.description = data.description
    if data.is_active is not None:
        role.is_active = data.is_active
    if data.permissions is not None:
        role_accesses = db.query(Accesses).filter(Accesses.role_id == data.id).all()
        role_permissions = [access.permission_id for access in role_accesses]
        for permission in role_permissions:
            if permission not in data.permissions:
                access = db.query(Accesses).filter(
                    and_(
                        Accesses.role_id == data.id,
                        Accesses.permission_id == permission
                    )
                ).first()
                db.delete(access)
                db.flush()

        for permission in data.permissions:
            if permission not in role_permissions:
                access = Accesses(
                    permission_id=permission,
                    role_id=role.id
                )
                db.add(access)
                db.flush()

        db.commit()
        db.refresh(role)

    return role
