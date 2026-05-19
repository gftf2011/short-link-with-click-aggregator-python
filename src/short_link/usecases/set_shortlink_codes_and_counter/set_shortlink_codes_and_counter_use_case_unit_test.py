import pytest
from unittest.mock import AsyncMock, Mock
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.usecases.set_shortlink_codes_and_counter.set_shortlink_codes_and_counter_use_case import (
    SetShortlinkCodesAndCounterUseCase,
    SetShortlinkCodesAndCounterUseCaseInput,
)


@pytest.mark.asyncio
async def test_given_empty_codes_input_when_calls_execute_then_should_call_only_set_counter():
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.set_shortlink_codes = AsyncMock(return_value=None)
    shortlink_gateway.set_counter = AsyncMock(return_value=None)
    use_case = SetShortlinkCodesAndCounterUseCase(shortlink_gateway=shortlink_gateway)
    input = SetShortlinkCodesAndCounterUseCaseInput(codes=[], counter="0000000")
    result = await use_case.execute(input)
    assert result is None
    shortlink_gateway.set_shortlink_codes.assert_not_called()
    shortlink_gateway.set_counter.assert_called_once_with("0000000")


@pytest.mark.asyncio
async def test_given_no_counter_input_when_calls_execute_then_should_call_only_set_shortlink_codes():
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.set_shortlink_codes = AsyncMock(return_value=None)
    shortlink_gateway.set_counter = AsyncMock(return_value=None)
    use_case = SetShortlinkCodesAndCounterUseCase(shortlink_gateway=shortlink_gateway)
    input = SetShortlinkCodesAndCounterUseCaseInput(
        codes=["a1b2c3d", "a1b2c3e", "a1b2c3f"], counter=None
    )
    result = await use_case.execute(input)
    assert result is None
    shortlink_gateway.set_shortlink_codes.assert_called_once_with(
        ["a1b2c3d", "a1b2c3e", "a1b2c3f"]
    )
    shortlink_gateway.set_counter.assert_not_called()
