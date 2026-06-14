from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def broadcast(self, message: dict, room: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@router.websocket("/ws/order/{order_id}")
async def order_tracking(websocket: WebSocket, order_id: int):
    room = f"order_{order_id}"
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.loads(data), room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)

@router.websocket("/ws/driver/{driver_id}")
async def driver_location(websocket: WebSocket, driver_id: int):
    room = f"driver_{driver_id}"
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.loads(data), room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)