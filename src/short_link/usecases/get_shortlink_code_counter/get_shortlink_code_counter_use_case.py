from shared.constants.base import BASE
from shared.constants.base_62 import BASE62
from shared.usecases.usecase import UseCase
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway


class GetShortlinkCodeCounterUseCase(UseCase[None, int]):
    def __init__(self, shortlink_gateway: ShortLinkGateway):
        self.shortlink_gateway = shortlink_gateway

    async def execute(self, input: None) -> int:
        value = await self.shortlink_gateway.get_counter()
        if value is None:
            return 0
        code_counter = 0
        for char in value:
            code_counter = code_counter * BASE + BASE62.index(char)
        return code_counter
