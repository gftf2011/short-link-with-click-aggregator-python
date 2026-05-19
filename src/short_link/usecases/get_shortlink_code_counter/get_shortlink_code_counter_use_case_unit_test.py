import pytest

from unittest.mock import AsyncMock, Mock

from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.usecases.get_shortlink_code_counter.get_shortlink_code_counter_use_case import (
    GetShortlinkCodeCounterUseCase,
)


@pytest.mark.asyncio
async def test_given_no_input_when_calls_execute_and_get_counter_returns_None_then_should_return_0():
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_counter = AsyncMock(return_value=None)
    use_case = GetShortlinkCodeCounterUseCase(shortlink_gateway=shortlink_gateway)
    result = await use_case.execute(None)
    assert result == 0
    shortlink_gateway.get_counter.assert_called_once_with()


@pytest.mark.asyncio
async def test_given_no_input_when_calls_execute_and_get_counter_returns_value_ZZZZZZZ_then_should_return_value_3521614606207():
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_counter = AsyncMock(return_value="ZZZZZZZ")
    use_case = GetShortlinkCodeCounterUseCase(shortlink_gateway=shortlink_gateway)
    result = await use_case.execute(None)
    assert result == 3521614606207
    shortlink_gateway.get_counter.assert_called_once_with()


@pytest.mark.asyncio
async def test_given_no_input_when_calls_execute_and_get_counter_returns_value_0000000_then_should_return_value_0():
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_counter = AsyncMock(return_value="0000000")
    use_case = GetShortlinkCodeCounterUseCase(shortlink_gateway=shortlink_gateway)
    result = await use_case.execute(None)
    assert result == 0
    shortlink_gateway.get_counter.assert_called_once_with()
