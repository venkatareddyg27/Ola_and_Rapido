from typing import Dict
from fastapi import (WebSocket)


class WebSocketManager:

    def __init__(self):
        self.active_connections: Dict[str,WebSocket] = {}

    async def connect(self,user_id: str,websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(
            f" WebSocket Connected: {user_id}")

    async def disconnect(self,user_id: str):
        if user_id in (self.active_connections):
            del self.active_connections[user_id]
            print(
                f" WebSocket Disconnected: "
                f"{user_id}")

    async def send_to_user(self,user_id: str,message: dict):
        websocket = (self.active_connections.get(user_id))
        if websocket:
            await websocket.send_json(message)

    async def broadcast(self,message: dict):
        for websocket in (self.active_connections.values()):
            await websocket.send_json(message)

    async def broadcast_excluding(self,message: dict,excluded_user_id: str):
        for (user_id,websocket) in (self.active_connections.items()):
            if (user_id !=excluded_user_id):
                await websocket.send_json(message)

    def is_connected(self,user_id: str) -> bool:

        return (user_id in self.active_connections)


websocket_manager = WebSocketManager()