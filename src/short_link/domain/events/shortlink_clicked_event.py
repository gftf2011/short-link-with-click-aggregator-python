from dataclasses import dataclass, field
from datetime import datetime, timezone

from shared.domain.event import Event


@dataclass
class ShortlinkClickedEvent(Event):
    name: str = field(default="ShortlinkClickedEvent", init=False)
    short_code: str
    clicked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
