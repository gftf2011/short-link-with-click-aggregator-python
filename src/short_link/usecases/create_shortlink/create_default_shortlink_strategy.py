from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from shared.usecases.exceptions import ApplicationException
from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.usecases.create_shortlink.create_shortlink_strategy import (
    CreateShortlinkStrategy,
)
from short_link.usecases.create_shortlink.create_shortlink_types import (
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)


class CreateDefaultShortlinkStrategy(CreateShortlinkStrategy):
    def __init__(
        self,
        short_link_repository: ShortLinkRepository,
        shortlink_gateway: ShortLinkGateway,
    ):
        self.short_link_repository = short_link_repository
        self.shortlink_gateway = shortlink_gateway

    async def execute(
        self, input: CreateShortLinkUseCaseInput
    ) -> CreateShortLinkUseCaseOutput:
        try:
            short_link: ShortLinkAggregate | None = (
                await self.shortlink_gateway.get_shortlink(input.url, input.expires_at)
            )
            if short_link is None:
                raise ApplicationException("Failed to generate shortlink")
            self.short_link_repository.create(short_link)
            return CreateShortLinkUseCaseOutput(code=short_link.short_code)
        except Exception as e:
            raise e
