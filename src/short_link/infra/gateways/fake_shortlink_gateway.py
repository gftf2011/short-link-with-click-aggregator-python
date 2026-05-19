from datetime import datetime

from shared.constants.base import BASE
from shared.constants.base_62 import BASE62
from shared.utils.encode_fixed_base62 import encode_int_to_fixed_base62
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.domain.utils.shortlink_code_list import ShortLinkCodeList


class FakeShortLinkGateway(ShortLinkGateway):
    def __init__(self) -> None:
        self._counter: str | None = None
        self._codes: list[str] = []

    @staticmethod
    def _decode_counter(value: str) -> int:
        code_counter = 0
        for char in value:
            code_counter = code_counter * BASE + BASE62.index(char)
        return code_counter

    @property
    def counter(self) -> int:
        if self._counter is None:
            return 0
        return self._decode_counter(self._counter)

    @property
    def codes(self) -> list[str]:
        return list(self._codes)

    async def get_counter(self) -> str | None:
        return self._counter

    async def set_counter(self, counter: str) -> None:
        self._counter = counter

    def generate(self, num: int) -> str:
        return encode_int_to_fixed_base62(num)

    async def set_shortlink_codes(self, codes: list[str]) -> None:
        for code in codes:
            self._codes.insert(0, code)

    async def get_shortlink(
        self, url: str, expires_at: datetime
    ) -> ShortLinkAggregate | None:
        async with ShortLinkCodeList.mutation_lock():
            if ShortLinkCodeList.is_empty():
                codes: list[str] | None = self._codes
                ShortLinkCodeList.add(codes)

            code = ShortLinkCodeList.pop()
        if code:
            return ShortLinkAggregate.create_new(
                short_code=code, url=url, expires_at=expires_at, is_custom=False
            )
        return None
