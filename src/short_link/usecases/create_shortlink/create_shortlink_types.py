from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateShortLinkUseCaseInput:
    url: str
    expires_at: datetime
    alias: str | None = None


@dataclass
class CreateShortLinkUseCaseOutput:
    code: str
