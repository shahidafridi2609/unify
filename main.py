import ast
import json
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "unify/static"),
    name="static",
)


conn_with_ids={}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket,ClientID):
        await websocket.accept()
        conn_with_ids[ClientID]=websocket
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket,ClientID):
        conn_with_ids.pop(ClientID)
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_msg_client(self, message: str,ClientID):
        await conn_with_ids[int(ClientID)].send_text(message)
        '''for connection in self.active_connections:
            print('sasa',connection)
            await connection.send_text(message)'''



manager = ConnectionManager()


@app.get("/")
async def get(request:Request):
    return templates.TemplateResponse("UI.html",{"request":request})


@app.websocket("/EstablishConn/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket,client_id)
    try:
        while True:
            print(conn_with_ids)
            data = await websocket.receive_text()
            data=ast.literal_eval(data)
            print(data)
            #await manager.send_personal_message(f"You wrote: {data['msg']", websocket)
            await manager.send_msg_client(data['msg'],data['friend_id'])
    except WebSocketDisconnect:
        manager.disconnect(websocket,client_id)
        await manager.send_msg_client(f"Client #{client_id} left the chat",client_id)
