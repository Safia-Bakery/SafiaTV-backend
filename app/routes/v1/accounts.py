from uuid import UUID

from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException
)
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session

from app.crud.accounts import get_account_by_password, get_account_list, create_account, get_account_by_id, edit_account
from app.routes.depth import get_db, PermissionChecker, get_me
from app.schemas.accounts import CreateAccount, GetAccountFullData, AccountLogin, GetAccounts, UpdateAccount
from app.utils.utils import verify_password, create_access_token, create_refresh_token, hash_password


account_router = APIRouter()


@account_router.post('/accounts/login')
async def account_login(
        # form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        data: AccountLogin,
        db: Session = Depends(get_db)
):
    account = get_account_by_password(db=db, password=data.password)
    if not account:
        raise HTTPException(status_code=404, detail="Invalid password")

    # if not verify_password(data.password, account.password):
    #     raise HTTPException(status_code=404, detail="Invalid password")

    permissions = []
    if account.role.accesses:
        for access in account.role.accesses:
            permissions.append(access.permission.link)
        account_info = {
            "id": str(account.id),
            "password": account.password,
            "branch_id": str(account.branch_id),
            "account_group": str(account.accountgroup_id)
        }

        return {
            "access_token": create_access_token(subject=account.password, permissions=permissions, account_info=account_info),
            "refresh_token": create_refresh_token(subject=account.password, permissions=permissions, account_info=account_info)
        }
    return None


@account_router.post('/accounts', response_model=GetAccountFullData)
async def add_account(
        data: CreateAccount,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='create_account'))
):
    account = get_account_by_password(db=db, password=data.password)
    if account:
        raise HTTPException(status_code=404, detail="Account with this password already exists")

    created_account = create_account(
        db=db,
        password=data.password,
        role_id=data.role_id,
        accountgroup_id=data.accountgroup_id,
        branch_id=data.branch_id
    )
    return created_account




@account_router.get('/accounts/me', response_model=GetAccountFullData)
async def get_me(
        db: Session = Depends(get_db),
        current_user: GetAccountFullData = Depends(get_me)
):
    return current_user


@account_router.get("/accounts", response_model=Page[GetAccounts])
async def get_accounts(
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_account'))
):
    return paginate(get_account_list(db=db))


@account_router.get("/accounts/{id}", response_model=GetAccountFullData)
async def get_account(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_account'))
):
    return get_account_by_id(db=db, id=id)



@account_router.put("/accounts", response_model=GetAccountFullData)
async def update_account(
        data: UpdateAccount,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='edit_account'))
):
    return edit_account(db=db, data=data)
