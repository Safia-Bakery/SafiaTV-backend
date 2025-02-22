from typing import Dict

from fastapi import HTTPException, WebSocket




class ConnectionManager:
    active_connections: Dict[str, WebSocket] = {}

    async def connect(self, account_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[account_id] = websocket
        print(f"Account {account_id} is connected.")

    def disconnect(self, account_id: str):
        """Remove a disconnected WebSocket connection."""
        if account_id in self.active_connections:
            del self.active_connections[account_id]
            print(f"Account {account_id} is disconnected.")

    async def send_text(self, account_id: str, data: str):
        """Send specific data to a connected screen by screen_id."""
        if account_id in self.active_connections:
            websocket = self.active_connections[account_id]
            await websocket.send_text(data)
            print(f"Sent to account {account_id}: {data}")
        else:
            raise HTTPException(status_code=404, detail=f"Account {account_id} is not connected.")

    async def send_json(self, account_id: str, data: dict):
        """Send specific data to a connected screen by screen_id."""
        if account_id in self.active_connections:
            websocket = self.active_connections[account_id]
            await websocket.send_json(data=data)
        else:
            raise HTTPException(status_code=404, detail=f"Account {account_id} is not connected.")

    async def broadcast(self, data: str):
        """Broadcast data to all connected screens."""
        for account_id, websocket in self.active_connections.items():
            await websocket.send_text(data)
            print(f"Broadcasted to {account_id}: {data}")


# Instantiate the ConnectionManager
manager = ConnectionManager()



