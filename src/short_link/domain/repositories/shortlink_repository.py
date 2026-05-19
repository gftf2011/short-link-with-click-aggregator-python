from abc import ABC

from short_link.domain.shortlink_aggregate import ShortLinkAggregate


class ShortLinkRepository(ABC):
    async def get_by_code(self, code: str) -> ShortLinkAggregate | None:
        raise NotImplementedError

    def create(self, short_link: ShortLinkAggregate) -> None:
        raise NotImplementedError
