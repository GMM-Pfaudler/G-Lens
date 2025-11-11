# app/core/sse_event_sender.py
import asyncio
import json

class EventBroker:
    def __init__(self):
        self.listeners: list[asyncio.Queue] = []

    async def push(self, data: dict):
        """Push event to all queues."""
        for queue in self.listeners:
            await queue.put(data)

    async def subscribe(self):
        """Create a new queue for an SSE connection."""
        queue = asyncio.Queue()
        self.listeners.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        """Remove a queue when client disconnects."""
        if queue in self.listeners:
            self.listeners.remove(queue)

# Instantiate globally (singleton)
broker = EventBroker()
