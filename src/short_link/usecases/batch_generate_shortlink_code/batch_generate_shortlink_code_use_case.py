from dataclasses import dataclass
from shared.domain.notification import Notification
from shared.usecases.usecase import UseCase
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.domain.validators.short_code.short_code_validatior_pipeline import (
    ShortCodeValidatorPipeline as ShortCodeValidator,
)


@dataclass
class BatchGenerateShortlinkCodeUseCaseInput:
    start: int
    end: int


@dataclass
class BatchGenerateShortlinkCodeUseCaseOutput:
    codes: list[str]
    last_code: str | None


class BatchGenerateShortlinkCodeUseCase(
    UseCase[
        BatchGenerateShortlinkCodeUseCaseInput, BatchGenerateShortlinkCodeUseCaseOutput
    ]
):
    def __init__(self, shortlink_gateway: ShortLinkGateway):
        self.shortlink_gateway = shortlink_gateway

    async def execute(
        self, input: BatchGenerateShortlinkCodeUseCaseInput
    ) -> BatchGenerateShortlinkCodeUseCaseOutput:
        last_code = None
        codes: list[str] = []
        notification = Notification()
        for num in range(input.start, input.end):
            last_code = self.shortlink_gateway.generate(num)
            ShortCodeValidator.validate(last_code, False, notification)
            if notification.has_exceptions():
                notification.clear_exceptions()
                continue
            codes.append(last_code)

        return BatchGenerateShortlinkCodeUseCaseOutput(codes=codes, last_code=last_code)
