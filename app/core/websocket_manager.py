
from typing import Dict

from fastapi import (
    WebSocket,
    WebSocketDisconnect
)


class WebSocketManager:

    def __init__(self):

        # ================================================
        # ACTIVE CONNECTIONS
        # ================================================

        self.active_connections: Dict[
            str,
            WebSocket
        ] = {}

    # ====================================================
    # CONNECT
    # ====================================================

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[
            user_id
        ] = websocket

        print(
            f"✅ WebSocket Connected: {user_id}"
        )

    # ====================================================
    # DISCONNECT
    # ====================================================

    async def disconnect(
        self,
        user_id: str
    ):

        if user_id in (
            self.active_connections
        ):

            del self.active_connections[
                user_id
            ]

            print(
                f"❌ WebSocket Disconnected: "
                f"{user_id}"
            )

    # ====================================================
    # SEND TO SINGLE USER
    # ====================================================

    async def send_to_user(
        self,
        user_id: str,
        message: dict
    ):

        websocket = (
            self.active_connections.get(
                user_id
            )
        )

        if websocket:

            await websocket.send_json(
                message
            )

    # ====================================================
    # BROADCAST TO ALL USERS
    # ====================================================

    async def broadcast(
        self,
        message: dict
    ):

        for websocket in (
            self.active_connections
            .values()
        ):

            await websocket.send_json(
                message
            )

    # ====================================================
    # BROADCAST EXCLUDING USER
    # ====================================================

    async def broadcast_excluding(
        self,
        message: dict,
        excluded_user_id: str
    ):

        for (
            user_id,
            websocket
        ) in (
            self.active_connections
            .items()
        ):

            if (
                user_id !=
                excluded_user_id
            ):

                await websocket.send_json(
                    message
                )

    # ====================================================
    # CHECK USER ONLINE
    # ====================================================

    def is_connected(
        self,
        user_id: str
    ) -> bool:

        return (
            user_id in
            self.active_connections
        )


# =========================================================
# GLOBAL INSTANCE
# =========================================================

websocket_manager = WebSocketManager()