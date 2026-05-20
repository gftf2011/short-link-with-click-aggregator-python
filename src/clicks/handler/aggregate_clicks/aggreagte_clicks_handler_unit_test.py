import pytest

from unittest.mock import AsyncMock, Mock

from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from clicks.handler.aggregate_clicks.aggregate_clicks_handler import (
    AggregateClicksHandler,
)


@pytest.mark.asyncio
async def test_given_empty_buffer_when_calls_handle_then_should_return_empty_dict():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = AsyncMock(return_value=[])
    handler = AggregateClicksHandler(buffer=buffer)

    result = await handler.handle(None)

    assert result == {}
    buffer.drain.assert_awaited_once()


@pytest.mark.asyncio
async def test_given_single_short_code_when_calls_handle_then_should_return_count_of_one():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = AsyncMock(return_value=["a1b2c3d"])
    handler = AggregateClicksHandler(buffer=buffer)

    result = await handler.handle(None)

    assert result == {"a1b2c3d": 1}


@pytest.mark.asyncio
async def test_given_repeated_short_code_when_calls_handle_then_should_sum_occurrences():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = AsyncMock(return_value=["a1b2c3d", "a1b2c3d", "a1b2c3d"])
    handler = AggregateClicksHandler(buffer=buffer)

    result = await handler.handle(None)

    assert result == {"a1b2c3d": 3}


@pytest.mark.asyncio
async def test_given_multiple_short_codes_when_calls_handle_then_should_map_each_count():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = AsyncMock(return_value=["a1b2c3d", "b2c3d4e", "a1b2c3d", "a1b2c3d", "b2c3d4e"])
    handler = AggregateClicksHandler(buffer=buffer)

    result = await handler.handle(None)

    assert result == {"a1b2c3d": 3, "b2c3d4e": 2}


@pytest.mark.asyncio
async def test_given_buffer_raises_when_calls_handle_then_should_propagate_exception():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = AsyncMock(side_effect=Exception("drain error"))
    handler = AggregateClicksHandler(buffer=buffer)

    with pytest.raises(Exception, match="drain error"):
        await handler.handle(None)
