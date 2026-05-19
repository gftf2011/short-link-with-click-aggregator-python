from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ShortLinkCacheValueDTO(BaseModel):
    id: UUID
    short_code: str
    url: str
    created_at: datetime
    expires_at: datetime
    is_custom: bool
