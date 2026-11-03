from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import RoomManager

app = FastAPI()
manager = RoomManager()

@app.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    is_connected = await manager.connect(websocket, room_code)
    if not is_connected:
        return

    players_count = len(manager.rooms[room_code])
    await manager.broadcast_to_room(
        room_code, 
        {"status": f"Player joined. ({players_count}/2)"}
    )

    try:
        while True:
            data = await websocket.receive_json()
            
            await manager.broadcast_to_room(room_code, {"event": "new_move", "data": data})

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code)
        await manager.broadcast_to_room(
            room_code, 
            {"error": "The opponent has disconnected. The game has been stopped."}
        )