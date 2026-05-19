import re
import pytest

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from shared.usecases.exceptions import ApplicationException
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.usecases.create_shortlink.create_shortlink_use_case import (
    CreateShortLinkUseCase,
    CreateShortLinkUseCaseInput,
)


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_then_should_return_short_code():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    aggregate = ShortLinkAggregate(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        expires_at=expires_at,
        is_custom=False,
    )
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(return_value=None)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_shortlink = AsyncMock(return_value=aggregate)
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at
    )
    result = await use_case.execute(input)
    short_link_repository.create.assert_called_once_with(aggregate)
    assert result.code == "a1b2c3d"
    assert shortlink_gateway.get_shortlink.call_count == 1
    gw_url, gw_expires_at = shortlink_gateway.get_shortlink.call_args[0]
    assert gw_url == input.url
    assert isinstance(gw_expires_at, datetime)
    assert gw_expires_at == expires_at


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_is_custom_then_should_return_short_code():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(return_value=None)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at, alias="my-brand"
    )
    result = await use_case.execute(input)
    assert shortlink_gateway.get_shortlink.call_count == 0
    assert result.code == "my-brand"


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_does_not_find_short_link_then_should_raise_exception():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(return_value=None)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_shortlink = AsyncMock(return_value=None)
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at
    )
    with pytest.raises(
        ApplicationException, match=re.escape("Failed to generate shortlink")
    ):
        await use_case.execute(input)
    short_link_repository.create.assert_not_called()
    assert shortlink_gateway.get_shortlink.call_count == 1
    gw_url, gw_expires_at = shortlink_gateway.get_shortlink.call_args[0]
    assert gw_url == input.url
    assert isinstance(gw_expires_at, datetime)


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_repository_raises_exception_then_should_raise_exception():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    aggregate = ShortLinkAggregate(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        expires_at=expires_at,
    )
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(side_effect=Exception("Repository error"))
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_shortlink = AsyncMock(return_value=aggregate)
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at
    )
    with pytest.raises(Exception, match=re.escape("Repository error")):
        await use_case.execute(input)
    assert shortlink_gateway.get_shortlink.call_count == 1
    gw_url, gw_expires_at = shortlink_gateway.get_shortlink.call_args[0]
    assert gw_url == input.url
    assert isinstance(gw_expires_at, datetime)
    short_link_repository.create.assert_called_once_with(aggregate)


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_execute_and_gateway_raises_exception_then_should_raise_exception():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(return_value=None)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_shortlink = AsyncMock(side_effect=Exception("Gateway error"))
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at
    )
    with pytest.raises(Exception, match=re.escape("Gateway error")):
        await use_case.execute(input)
    assert shortlink_gateway.get_shortlink.call_count == 1
    gw_url, gw_expires_at = shortlink_gateway.get_shortlink.call_args[0]
    assert gw_url == input.url
    assert isinstance(gw_expires_at, datetime)
    short_link_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_given_expires_at_when_calls_execute_then_should_pass_same_to_gateway():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    aggregate = ShortLinkAggregate(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        expires_at=expires_at,
    )
    short_link_repository = Mock(spec=ShortLinkRepository)
    short_link_repository.create = Mock(return_value=None)
    shortlink_gateway = Mock(spec=ShortLinkGateway)
    shortlink_gateway.get_shortlink = AsyncMock(return_value=aggregate)
    use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository, shortlink_gateway=shortlink_gateway
    )
    input = CreateShortLinkUseCaseInput(
        url="https://example.com", expires_at=expires_at
    )
    await use_case.execute(input)
    shortlink_gateway.get_shortlink.assert_called_once_with(
        "https://example.com", expires_at
    )
