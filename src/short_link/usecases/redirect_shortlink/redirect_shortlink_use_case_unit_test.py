import re
import pytest

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent
from shared.domain.exceptions import DomainException
from shared.handlers.mediator import Mediator
from shared.usecases.exceptions import ApplicationException
from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.usecases.redirect_shortlink.redirect_shortlink_use_case import (
    RedirectShortLinkUseCase,
    RedirectShortLinkUseCaseInput,
)


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_then_should_return_url():
    expires = datetime.now(timezone.utc) + timedelta(days=1)
    created = datetime.now(timezone.utc)
    aggregate = ShortLinkAggregate.create_from_datasource(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        created_at=created,
        expires_at=expires,
        is_custom=False,
    )
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.get_by_code = AsyncMock(return_value=aggregate)
    mediator = Mock(spec=Mediator)
    use_case = RedirectShortLinkUseCase(short_link_repository=short_link_repository, mediator=mediator)
    result = await use_case.execute(RedirectShortLinkUseCaseInput(code="a1b2c3d"))
    assert result.url == "https://example.com"
    short_link_repository.get_by_code.assert_awaited_once_with("a1b2c3d")
    mediator.publish.assert_called_once()
    [event] = mediator.publish.call_args[0][0]
    assert isinstance(event, ShortlinkClickedEvent)
    assert event.short_code == "a1b2c3d"


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_does_not_find_short_link_then_should_raise_exception():
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.get_by_code = AsyncMock(return_value=None)
    mediator = Mock(spec=Mediator)
    use_case = RedirectShortLinkUseCase(short_link_repository=short_link_repository, mediator=mediator)
    with pytest.raises(
        ApplicationException, match=re.escape("Short link not found for code: a1b2c3d")
    ):
        await use_case.execute(RedirectShortLinkUseCaseInput(code="a1b2c3d"))
    short_link_repository.get_by_code.assert_awaited_once_with("a1b2c3d")
    mediator.publish.assert_not_called()


@pytest.mark.asyncio
async def test_given_short_link_expired_when_calls_execute_then_should_raise_domain_exception():
    expires = datetime.now(timezone.utc) - timedelta(seconds=1)
    created = datetime.now(timezone.utc) - timedelta(days=1)
    aggregate = ShortLinkAggregate.create_from_datasource(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        created_at=created,
        expires_at=expires,
        is_custom=False,
    )
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.get_by_code = AsyncMock(return_value=aggregate)
    mediator = Mock(spec=Mediator)
    use_case = RedirectShortLinkUseCase(short_link_repository=short_link_repository, mediator=mediator)
    with pytest.raises(
        DomainException, match=re.escape("expires_at cannot be in the past")
    ):
        await use_case.execute(RedirectShortLinkUseCaseInput(code="a1b2c3d"))
    short_link_repository.get_by_code.assert_awaited_once_with("a1b2c3d")
    mediator.publish.assert_not_called()


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_repository_raises_exception_then_should_raise_exception():
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.get_by_code = AsyncMock(
        side_effect=Exception("Repository error")
    )
    mediator = Mock(spec=Mediator)
    use_case = RedirectShortLinkUseCase(short_link_repository=short_link_repository, mediator=mediator)
    with pytest.raises(Exception, match=re.escape("Repository error")):
        await use_case.execute(RedirectShortLinkUseCaseInput(code="a1b2c3d"))
    short_link_repository.get_by_code.assert_awaited_once_with("a1b2c3d")
    mediator.publish.assert_not_called()
