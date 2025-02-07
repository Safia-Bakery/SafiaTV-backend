from sqlalchemy.orm import Session

from app.models.PermissionPages import PermissionPages
from app.models.Permissions import Permissions


def get_permission_page(db:Session, name):
    query = db.query(PermissionPages).filter(PermissionPages.name==name).first()
    return query


def create_permission_page(db:Session,name):
    query = PermissionPages(
        name=name
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_permission(db:Session,permission_page_id,link):
    query = db.query(Permissions).filter(Permissions.permission_page_id==permission_page_id,Permissions.link==link).first()
    return query

def get_permission_link(db:Session,link):
    query = db.query(Permissions).filter(Permissions.link==link).first()
    return query


def create_permission(db:Session,name,link,permission_page_id):
    query = Permissions(
        name=name,
        link=link,
        permission_page_id=permission_page_id
    )
    db.add(query)
    db.commit()
    return query


