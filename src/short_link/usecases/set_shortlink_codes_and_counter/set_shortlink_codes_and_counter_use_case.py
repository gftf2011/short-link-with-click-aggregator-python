from dataclasses import dataclass
from shared.usecases.usecase import UseCase
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway


@dataclass
class SetShortlinkCodesAndCounterUseCaseInput:
    codes: list[str]
    counter: str | None


class SetShortlinkCodesAndCounterUseCase(
    UseCase[SetShortlinkCodesAndCounterUseCaseInput, None]
):
    def __init__(self, shortlink_gateway: ShortLinkGateway):
        self.shortlink_gateway = shortlink_gateway

    async def execute(self, input: SetShortlinkCodesAndCounterUseCaseInput) -> None:
        if input.counter is not None:
            await self.shortlink_gateway.set_counter(input.counter)
        if input.codes:
            await self.shortlink_gateway.set_shortlink_codes(input.codes)
