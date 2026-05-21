import pytest

from unittest.mock import AsyncMock, Mock

from clicks.domain.aggregator.clicks_aggregator import ClicksAggregator
from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from clicks.handler.aggregate_clicks.aggregate_clicks_handler import (
    AggregateClicksHandler,
)


@pytest.mark.asyncio
async def test_given_empty_buffer_when_calls_handle_then_should_aggregate_empty_dict():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(return_value=[])
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock()
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    await handler.handle(None)

    buffer.drain.assert_called_once()
    aggregator.aggregate.assert_awaited_once_with({})


@pytest.mark.asyncio
async def test_given_single_short_code_when_calls_handle_then_should_aggregate_count_of_one():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(return_value=["a1b2c3d"])
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock()
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    await handler.handle(None)

    aggregator.aggregate.assert_awaited_once_with({"a1b2c3d": 1})


@pytest.mark.asyncio
async def test_given_repeated_short_code_when_calls_handle_then_should_aggregate_summed_count():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(return_value=["a1b2c3d", "a1b2c3d", "a1b2c3d"])
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock()
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    await handler.handle(None)

    aggregator.aggregate.assert_awaited_once_with({"a1b2c3d": 3})


@pytest.mark.asyncio
async def test_given_multiple_short_codes_when_calls_handle_then_should_aggregate_each_count():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(
        return_value=["a1b2c3d", "b2c3d4e", "a1b2c3d", "a1b2c3d", "b2c3d4e"]
    )
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock()
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    await handler.handle(None)

    aggregator.aggregate.assert_awaited_once_with({"a1b2c3d": 3, "b2c3d4e": 2})


@pytest.mark.asyncio
async def test_given_buffer_raises_when_calls_handle_then_should_propagate_exception():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(side_effect=Exception("drain error"))
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock()
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    with pytest.raises(Exception, match="drain error"):
        await handler.handle(None)

    aggregator.aggregate.assert_not_awaited()


@pytest.mark.asyncio
async def test_given_aggregator_raises_when_calls_handle_then_should_propagate_exception():
    buffer = Mock(spec=ClicksBuffer)
    buffer.drain = Mock(return_value=["a1b2c3d"])
    aggregator = Mock(spec=ClicksAggregator)
    aggregator.aggregate = AsyncMock(side_effect=Exception("aggregator error"))
    handler = AggregateClicksHandler(buffer=buffer, aggregator=aggregator)

    with pytest.raises(Exception, match="aggregator error"):
        await handler.handle(None)
