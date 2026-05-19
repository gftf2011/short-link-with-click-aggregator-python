from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCase,
    BatchGenerateShortlinkCodeUseCaseInput,
)
from short_link.usecases.get_shortlink_code_counter.get_shortlink_code_counter_use_case import (
    GetShortlinkCodeCounterUseCase,
)
from short_link.usecases.set_shortlink_codes_and_counter.set_shortlink_codes_and_counter_use_case import (
    SetShortlinkCodesAndCounterUseCase,
    SetShortlinkCodesAndCounterUseCaseInput,
)


class BatchController:
    def __init__(
        self,
        max: int,
        chunk_size: int,
        set_shortlink_codes_and_counter_use_case: SetShortlinkCodesAndCounterUseCase,
        get_shortlink_code_counter_use_case: GetShortlinkCodeCounterUseCase,
        batch_generate_shortlink_code_use_case: BatchGenerateShortlinkCodeUseCase,
    ):
        self.max = max
        self.chunk_size = chunk_size
        self.set_shortlink_codes_and_counter_use_case = (
            set_shortlink_codes_and_counter_use_case
        )
        self.get_shortlink_code_counter_use_case = get_shortlink_code_counter_use_case
        self.batch_generate_shortlink_code_use_case = (
            batch_generate_shortlink_code_use_case
        )

    async def _batch_process(self, start: int, end: int):
        batch_result = await self.batch_generate_shortlink_code_use_case.execute(
            BatchGenerateShortlinkCodeUseCaseInput(start=start, end=end)
        )
        await self.set_shortlink_codes_and_counter_use_case.execute(
            SetShortlinkCodesAndCounterUseCaseInput(
                codes=batch_result.codes,
                counter=batch_result.last_code,
            )
        )

    async def run(self):
        counter = await self.get_shortlink_code_counter_use_case.execute(None)
        limit = self.max + counter

        while counter + self.chunk_size <= limit:
            await self._batch_process(counter, counter + self.chunk_size)
            counter += self.chunk_size

        if counter < limit:
            await self._batch_process(counter, limit)
