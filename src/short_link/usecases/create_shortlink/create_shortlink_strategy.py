from abc import ABC, abstractmethod

from short_link.usecases.create_shortlink.create_shortlink_types import (
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)


class CreateShortlinkStrategy(ABC):
    @abstractmethod
    async def execute(
        self, input: CreateShortLinkUseCaseInput
    ) -> CreateShortLinkUseCaseOutput:
        pass
