from dataclasses import dataclass

from shared.usecases.exceptions import ApplicationException
from shared.usecases.usecase import UseCase
from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate


@dataclass
class RedirectShortLinkUseCaseInput:
    code: str


@dataclass
class RedirectShortLinkUseCaseOutput:
    url: str


class RedirectShortLinkUseCase(
    UseCase[RedirectShortLinkUseCaseInput, RedirectShortLinkUseCaseOutput]
):
    def __init__(self, short_link_repository: ShortLinkRepository):
        self.short_link_repository = short_link_repository

    async def execute(
        self, input: RedirectShortLinkUseCaseInput
    ) -> RedirectShortLinkUseCaseOutput:
        try:
            short_link: ShortLinkAggregate | None = (
                await self.short_link_repository.get_by_code(input.code)
            )
            if short_link is None:
                raise ApplicationException(
                    f"Short link not found for code: {input.code}"
                )
            short_link.validate_expires_at()
            return RedirectShortLinkUseCaseOutput(url=short_link.url)
        except Exception as e:
            raise e
