import asyncio
from datetime import datetime

from celery import Task

from clicks.handler.count_clicks.count_clicks_handler import CountClicksHandler
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent


class CeleryCountClicksTask(Task):
    name = "clicks.count_clicks"

    def __init__(self, handler: CountClicksHandler) -> None:
        super().__init__()
        self.handler = handler

    def run(self, event: dict) -> None:
        clicked_event = ShortlinkClickedEvent(
            short_code=event["short_code"],
            click_impression_id=event["click_impression_id"],
            clicked_at=datetime.fromisoformat(event["clicked_at"]),
        )
        asyncio.run(self.handler.handle(clicked_event))
