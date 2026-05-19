import pytest

from unittest.mock import Mock, call

from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCase,
    BatchGenerateShortlinkCodeUseCaseInput,
)


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_then_should_return_only_valid_codes():
    input = BatchGenerateShortlinkCodeUseCaseInput(start=116407978914, end=116407978917)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.generate = Mock(side_effect=["2340110", "2340111", "2340112"])
    use_case = BatchGenerateShortlinkCodeUseCase(shortlink_gateway=shortlink_gateway)
    result = await use_case.execute(input)
    assert len(result.codes) == 2
    assert result.codes == ["2340110", "2340112"]
    assert result.last_code == "2340112"
    shortlink_gateway.generate.assert_has_calls(
        [
            call(116407978914),
            call(116407978915),
            call(116407978916),
        ]
    )
