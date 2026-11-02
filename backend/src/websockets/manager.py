from fastapi import WebSocket

class RoomManager:
    def __init__(self):
        # Structure: {"room_123": [websocket1, websocket2]}
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_code: str) -> bool:
        await websocket.accept()
        
        if room_code not in self.rooms:
            self.rooms[room_code] = []
            
        if len(self.rooms[room_code]) >= 2:
            await websocket.send_json({"error": "Room is full"})
            await websocket.close()
            return False
            
        self.rooms[room_code].append(websocket)
        return True

    def disconnect(self, websocket: WebSocket, room_code: str):
        if room_code in self.rooms:
            if websocket in self.rooms[room_code]:
                self.rooms[room_code].remove(websocket)
            if not self.rooms[room_code]:
                del self.rooms[room_code]

    async def broadcast_to_room(self, room_code: str, message: dict):
        if room_code in self.rooms:
            for connection in self.rooms[room_code]:
                await connection.send_json(message)