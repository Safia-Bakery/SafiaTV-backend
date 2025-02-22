from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.websocket_connection import manager


websocket_router = APIRouter()



@websocket_router.websocket("/ws/{account_id}")
async def websocket_endpoint(websocket: WebSocket, account_id: str):
    """WebSocket connection handler."""
    await manager.connect(websocket)
    await manager.broadcast(f"Client {account_id} joined the chat")
    try:
        while True:
            client_message = await websocket.receive_text()
            await manager.broadcast(f"Client {account_id} says: {client_message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {account_id} left the chat")


