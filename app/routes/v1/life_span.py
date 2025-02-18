from contextlib import asynccontextmanager, contextmanager

import pytz
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.pages_and_permissions import (
    create_permission_page,
    create_permission,
    get_permission_page,
    get_permission,
    get_permission_link
)
from app.crud.roles import create_role, create_accesses, get_role_by_name
from app.crud.accounts import create_account, get_account_by_password
from app.db.session import SessionLocal
from app.routes.depth import get_db
from app.utils.permissions import pages_and_permissions

timezonetash = pytz.timezone('Asia/Tashkent')


#create new permission
@asynccontextmanager
async def create_permissions_lifespan():
    @contextmanager
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    with get_db() as db:
        for key, value in pages_and_permissions.items():
            permission_page = get_permission_page(db=db, name=key)
            if permission_page:
                permission_page_id = permission_page.id
            else:
                permission_page_id = create_permission_page(db=db, name=key).id
            for name, link in value.items():
                permission = get_permission(db=db, link=link, permission_page_id=permission_page_id)
                if not permission:
                    create_permission(db=db, name=name, link=link, permission_page_id=permission_page_id)

    yield  #--------------  HERE YOU CAN WRITE LOG ON CLOSING AFTER YIELD ------------


#---------------------- CREATE ROLE AND USERS FOR DEFAULT ADMIN USER --------------------------
@asynccontextmanager
async def create_role_lifespan():
    @contextmanager
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    with get_db() as db:
        role = get_role_by_name(db=db, name=settings.admin_role)
        if not role:
            role = create_role(db=db, name=settings.admin_role, description='Superuser')

        account = get_account_by_password(db=db, password=settings.admin_password)
        if not account:
            create_account(db=db, password=settings.admin_password, role_id=role.id)

    role_permissions = []
    for i in role.accesses:
        role_permissions.append(i.permission.link)

    for key, value in pages_and_permissions.items():
        for name, link in value.items():
            if link not in role_permissions:
                permission = get_permission_link(db=db, link=link)

                create_accesses(db=db, role_id=role.id, permission_id=permission.id)

    yield  #--------------  HERE YOU CAN WRITE LOG ON CLOSING AFTER YIELD ------------


# async def daily_run():
#     scheduler = BackgroundScheduler()
#
#     scheduler.start()
#     return True
#
#
# @asynccontextmanager
# async def run_scheduler():
#     await daily_run()
#     yield


@asynccontextmanager
async def combined_lifespan(app):
    async with create_permissions_lifespan(), create_role_lifespan():
        #-----------   BEFORE YIELD WHEN STARTING UP ALL THE FUNCTIONS WORK ---------
        yield
