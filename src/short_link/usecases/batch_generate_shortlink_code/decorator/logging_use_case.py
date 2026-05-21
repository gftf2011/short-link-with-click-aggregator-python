import json
import logging

from typing import Any
from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCase,
    BatchGenerateShortlinkCodeUseCaseOutput,
)
from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCaseInput,
)

logger = logging.getLogger(__name__)


class LoggingBatchGenerateShortlinkCodeUseCase(BatchGenerateShortlinkCodeUseCase):
    def __init__(
        self, batch_generate_shortlink_code_use_case: BatchGenerateShortlinkCodeUseCase
    ):
        self.batch_generate_shortlink_code_use_case = (
            batch_generate_shortlink_code_use_case
        )

    async def execute(
        self, input: BatchGenerateShortlinkCodeUseCaseInput
    ) -> BatchGenerateShortlinkCodeUseCaseOutput:
        log_data: dict[str, Any] = {}
        data = await self.batch_generate_shortlink_code_use_case.execute(input)
        if len(data.codes) > 0:
            log_data["input"] = {"start": input.start, "end": input.end}
            log_data["output"] = {"last_code": data.last_code}
            logger.info(json.dumps(log_data))
        return data
