from datetime import datetime
from typing import Union, Any

from app.crud.accounts import get_account_by_password
from app.schemas.accounts import GetAccountFullData
# from schemas import user_schema
# from queries import user_query as crud
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        permissions = payload.get('permissions')
        user = payload.get('user')
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user["permissions"] = permissions

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user




class PermissionChecker:

    def __init__(self, required_permissions: str) -> None:
        self.required_permissions = required_permissions

    def __call__(self,user :dict = Depends(get_current_user)) -> dict:
        if self.required_permissions not in user['permissions']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to use this api",
            )
        return user






async def get_me(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)) -> GetAccountFullData:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    account: Union[dict[str, Any], None] = get_account_by_password(db=db, password=sub)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find account",
        )

    return account
