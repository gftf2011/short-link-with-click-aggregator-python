from collections import Counter

from clicks.domain.aggregator.clicks_aggregator import ClicksAggregator
from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from shared.handlers.handler import Handler


class AggregateClicksHandler(Handler[None, None]):
    def __init__(self, buffer: ClicksBuffer, aggregator: ClicksAggregator) -> None:
        self.buffer = buffer
        self.aggregator = aggregator

    async def handle(self, input: None) -> None:
        items = await self.buffer.drain()
        counts = dict(Counter(items))
        await self.aggregator.aggregate(counts)
