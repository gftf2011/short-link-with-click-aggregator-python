from datetime import datetime, timedelta, timezone
from pydantic import BaseModel


class CreateShortLinkRequestDTO(BaseModel):
    url: str
    expires_at: datetime = datetime.now(timezone.utc) + timedelta(weeks=2)
    alias: str | None = None
