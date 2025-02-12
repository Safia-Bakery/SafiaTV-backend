from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.accounts import GetAccount



file_router = APIRouter()


@file_router.post("/file/upload",)
async def read_files(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    # current_user: GetAccount = Depends(get_current_user),
):
    file_path = f"files/{file.filename}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)

    return {"file_url": file_path}

