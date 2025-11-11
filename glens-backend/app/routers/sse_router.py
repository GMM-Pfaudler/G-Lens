from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.core.sse_event_sender import broker
import json

router = APIRouter(prefix="", tags=["SSE"])

@router.get("/db-updates")
async def stream_db_updates(request: Request):
    """Stream database update events via SSE."""
    queue = await broker.subscribe()

    async def event_stream():
        try:
            while True:
                # stop if client disconnects
                if await request.is_disconnected():
                    break
                data = await queue.get()  # wait for event
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            broker.unsubscribe(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
