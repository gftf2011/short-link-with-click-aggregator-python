from shared.usecases.usecase import UseCase
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.usecases.create_shortlink.create_shortlink_strategy import (
    CreateShortlinkStrategy,
)
from short_link.usecases.create_shortlink.create_custom_shortlink_strategy import (
    CreateCustomShortlinkStrategy,
)
from short_link.usecases.create_shortlink.create_default_shortlink_strategy import (
    CreateDefaultShortlinkStrategy,
)
from short_link.usecases.create_shortlink.create_shortlink_types import (
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)


class CreateShortLinkUseCase(
    UseCase[CreateShortLinkUseCaseInput, CreateShortLinkUseCaseOutput]
):
    def __init__(
        self,
        short_link_repository: ShortLinkRepository,
        shortlink_gateway: ShortLinkGateway,
    ):
        self.short_link_repository = short_link_repository
        self.shortlink_gateway = shortlink_gateway

    def _create_strategy(
        self, input: CreateShortLinkUseCaseInput
    ) -> CreateShortlinkStrategy:
        if input.alias:
            return CreateCustomShortlinkStrategy(self.short_link_repository)
        return CreateDefaultShortlinkStrategy(
            self.short_link_repository, self.shortlink_gateway
        )

    async def execute(
        self, input: CreateShortLinkUseCaseInput
    ) -> CreateShortLinkUseCaseOutput:
        try:
            strategy: CreateShortlinkStrategy = self._create_strategy(input)
            output = await strategy.execute(input)
            return output
        except Exception as e:
            raise e
