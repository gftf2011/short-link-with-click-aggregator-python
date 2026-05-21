from dataclasses import dataclass

from clicks.domain.repositories.clicks_repository import ClicksRepository
from shared.usecases.usecase import UseCase


@dataclass
class GetClicksCountByShortCodeUseCaseInput:
    short_code: str


@dataclass
class GetClicksCountByShortCodeUseCaseOutput:
    count: int


class GetClicksCountByShortCodeUseCase(
    UseCase[GetClicksCountByShortCodeUseCaseInput, GetClicksCountByShortCodeUseCaseOutput]
):
    def __init__(self, clicks_repository: ClicksRepository) -> None:
        self.clicks_repository = clicks_repository

    async def execute(
        self, input: GetClicksCountByShortCodeUseCaseInput
    ) -> GetClicksCountByShortCodeUseCaseOutput:
        count = await self.clicks_repository.get_clicks_by_short_code(input.short_code)
        return GetClicksCountByShortCodeUseCaseOutput(
            count=count,
        )
