# app/utils/ws_utils.py
from fastapi import WebSocket

ga_ws_connections: dict = {}

async def send_ws_message(ga_id: str, message: dict):
    conns = ga_ws_connections.get(ga_id, [])
    if not conns:
        return

    for ws in conns[:]:
        try:
            await ws.send_json(message)
        except Exception:
            try:
                conns.remove(ws)
            except ValueError:
                pass
    if not conns:
        ga_ws_connections.pop(ga_id, None)
