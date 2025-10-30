# app/core/ws_manager.py
from fastapi import WebSocket

# Centralized connection registry
connections: dict[str, list[WebSocket]] = {}

async def send_ws_message(job_id: str, message: dict):
    conns = connections.get(job_id, [])
    for ws in conns[:]:
        try:
            await ws.send_json(message)
        except Exception:
            conns.remove(ws)
    if not conns:
        connections.pop(job_id, None)

async def register_ws(job_id: str, ws: WebSocket):
    await ws.accept()
    if job_id not in connections:
        connections[job_id] = []
    connections[job_id].append(ws)

async def unregister_ws(job_id: str, ws: WebSocket):
    if job_id in connections and ws in connections[job_id]:
        connections[job_id].remove(ws)
    if not connections.get(job_id):
        connections.pop(job_id, None)
