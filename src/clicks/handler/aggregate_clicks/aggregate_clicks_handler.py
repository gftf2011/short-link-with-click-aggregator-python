from collections import Counter
from dataclasses import dataclass

from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from shared.handlers.handler import Handler



class AggregateClicksHandler(Handler[None, dict[str, int]]):
    def __init__(self, buffer: ClicksBuffer) -> None:
        self.buffer = buffer

    async def handle(self, input: None) -> dict[str, int]:
        items = await self.buffer.drain()
        return dict(Counter(items))
