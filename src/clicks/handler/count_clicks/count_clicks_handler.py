import asyncio

from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from shared.handlers.handler import Handler
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent


class CountClicksHandler(Handler[ShortlinkClickedEvent, None]):
    def __init__(self, buffer: ClicksBuffer) -> None:
        self.buffer = buffer

    async def handle(self, input: ShortlinkClickedEvent) -> None:
        await asyncio.to_thread(self.buffer.add, input.short_code, input.click_impression_id)
