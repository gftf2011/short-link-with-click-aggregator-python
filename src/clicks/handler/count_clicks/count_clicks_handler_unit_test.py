import pytest

from unittest.mock import Mock

from clicks.domain.buffer.clicks_buffer import ClicksBuffer
from clicks.handler.count_clicks.count_clicks_handler import CountClicksHandler
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent


@pytest.mark.asyncio
async def test_given_valid_event_when_calls_handle_then_should_add_short_code_to_buffer():
    buffer = Mock(spec=ClicksBuffer)
    handler = CountClicksHandler(buffer=buffer)
    event = ShortlinkClickedEvent(short_code="a1b2c3d")

    await handler.handle(event)

    buffer.add.assert_called_once_with("a1b2c3d")


@pytest.mark.asyncio
async def test_given_buffer_raises_when_calls_handle_then_should_propagate_exception():
    buffer = Mock(spec=ClicksBuffer)
    buffer.add.side_effect = Exception("buffer error")
    handler = CountClicksHandler(buffer=buffer)
    event = ShortlinkClickedEvent(short_code="a1b2c3d")

    with pytest.raises(Exception, match="buffer error"):
        await handler.handle(event)

    buffer.add.assert_called_once_with("a1b2c3d")
