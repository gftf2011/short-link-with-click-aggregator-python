import pytest

from short_link.infra.gateways.fake_shortlink_gateway import FakeShortLinkGateway
from short_link.presentation.batch.controller import BatchController
from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCase,
)
from short_link.usecases.get_shortlink_code_counter.get_shortlink_code_counter_use_case import (
    GetShortlinkCodeCounterUseCase,
)
from short_link.usecases.set_shortlink_codes_and_counter.set_shortlink_codes_and_counter_use_case import (
    SetShortlinkCodesAndCounterUseCase,
)


@pytest.mark.asyncio
async def test_given_no_input_when_calls_run_then_should_process_all_shortlink_codes():
    shortlink_gateway = FakeShortLinkGateway()
    set_shortlink_codes_and_counter_use_case = SetShortlinkCodesAndCounterUseCase(
        shortlink_gateway=shortlink_gateway
    )
    get_shortlink_code_counter_use_case = GetShortlinkCodeCounterUseCase(
        shortlink_gateway=shortlink_gateway
    )
    batch_generate_shortlink_code_use_case = BatchGenerateShortlinkCodeUseCase(
        shortlink_gateway=shortlink_gateway
    )
    max_index_exclusive = 14776399
    chunk_size = 1000
    controller = BatchController(
        max=max_index_exclusive,
        chunk_size=chunk_size,
        set_shortlink_codes_and_counter_use_case=set_shortlink_codes_and_counter_use_case,
        get_shortlink_code_counter_use_case=get_shortlink_code_counter_use_case,
        batch_generate_shortlink_code_use_case=batch_generate_shortlink_code_use_case,
    )
    await controller.run()
    assert shortlink_gateway.codes == ["0010010"]
    assert shortlink_gateway.counter == max_index_exclusive - 1
