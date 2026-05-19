from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.usecases.create_shortlink.create_shortlink_strategy import (
    CreateShortlinkStrategy,
)
from short_link.usecases.create_shortlink.create_shortlink_types import (
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)


class CreateCustomShortlinkStrategy(CreateShortlinkStrategy):
    def __init__(
        self,
        short_link_repository: ShortLinkRepository,
    ):
        self.short_link_repository = short_link_repository

    async def execute(
        self, input: CreateShortLinkUseCaseInput
    ) -> CreateShortLinkUseCaseOutput:
        try:
            short_link = ShortLinkAggregate.create_new(
                short_code=input.alias or "",
                url=input.url,
                expires_at=input.expires_at,
                is_custom=True,
            )
            self.short_link_repository.create(short_link)
            return CreateShortLinkUseCaseOutput(code=short_link.short_code)
        except Exception as e:
            raise e
