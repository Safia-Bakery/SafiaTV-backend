from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, WebSocketException
from sqlalchemy.orm import Session

from app.crud.media import get_device_medias
from app.routes.depth import PermissionChecker, get_db, get_current_user
from app.utils.websocket_connection import manager



websocket_router = APIRouter()


async def websocket_auth(websocket: WebSocket):
    """Extracts token from WebSocket headers and verifies authentication."""
    token = websocket.headers.get("Authorization")
    if not token:
        # raise WebSocketException(code=1008, reason="Token missing or invalid format")
        return None

    # token = token.split("Bearer ")[1]  # Extract actual token
    account = await get_current_user(token=token)

    if not account:
        return None

    return account  # Return decoded JWT data



@websocket_router.websocket("/ws/media/device")
async def websocket_endpoint(
        websocket: WebSocket,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions='view_media'))
):
    # Authenticate user
    current_user = await websocket_auth(websocket)
    print("current_user: ", current_user)
    if current_user is None:
        raise WebSocketException(code=1008, reason="Invalid or expired token")

    """WebSocket connection handler."""
    await manager.connect(account_id=current_user['id'], websocket=websocket)
    await manager.send_text(account_id=current_user['id'], data=f"Client {current_user['id']} is connected !")
    medias = get_device_medias(db=db, branch_id=current_user["branch_id"],
                               account_group=current_user["account_group"])
    data = {
        "items": [
            {
                "id": str(media.id),
                "name": media.name,
                "file_url": media.file_url,
                "description": media.description,
                "is_active": media.is_active,
                "accountgroup": {
                    "id": str(media.accountgroup.id),
                    "name": media.accountgroup.name,
                    "description": media.accountgroup.description,
                    "is_active": media.accountgroup.is_active
                },
                "created_at": str(media.created_at),
                "updated_at": str(media.updated_at)

            } for media in medias
        ]
    }
    try:
        await manager.send_json(account_id=current_user['id'], data=data)
        while True:
            client_message = await websocket.receive_text()
            await manager.broadcast(f"Client {current_user['id']} says: {client_message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {current_user['id']} is disconnected !")

