from abc import ABC
from datetime import datetime
from short_link.domain.shortlink_aggregate import ShortLinkAggregate


class ShortLinkGateway(ABC):
    async def get_counter(self) -> str | None:
        raise NotImplementedError

    async def set_counter(self, counter: str) -> None:
        raise NotImplementedError

    def generate(self, num: int) -> str:
        raise NotImplementedError

    async def get_shortlink(
        self, url: str, expires_at: datetime
    ) -> ShortLinkAggregate | None:
        raise NotImplementedError

    async def set_shortlink_codes(self, codes: list[str]) -> None:
        raise NotImplementedError
