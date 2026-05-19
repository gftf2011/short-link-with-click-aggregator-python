import re
from uuid import UUID

import pytest

from datetime import datetime, timedelta, timezone

from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from shared.domain.exceptions import DomainException


def test_given_valid_inputs_when_create_new_then_should_instantiate_shortlink_aggregate():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    aggregate = ShortLinkAggregate.create_new(
        short_code="a1b2c3d",
        url="https://example.com",
        expires_at=expires_at,
    )

    assert aggregate.id is not None
    assert aggregate.short_code == "a1b2c3d"
    assert aggregate.url == "https://example.com"
    assert aggregate.expires_at == expires_at
    assert aggregate.created_at is not None
    assert aggregate.is_custom == False


def test_given_valid_inputs_when_create_new_and_is_custom_then_should_instantiate_shortlink_aggregate():
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    aggregate = ShortLinkAggregate.create_new(
        short_code="my-brand",
        url="https://example.com",
        expires_at=expires_at,
        is_custom=True,
    )
    assert aggregate.id is not None
    assert aggregate.short_code == "my-brand"
    assert aggregate.url == "https://example.com"
    assert aggregate.expires_at == expires_at
    assert aggregate.created_at is not None
    assert aggregate.is_custom == True


def test_given_invalid_url_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(DomainException, match=re.escape("url is not a valid URL")):
        ShortLinkAggregate.create_new(
            short_code="a1b2c3d",
            url="invalid-url",
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            is_custom=False,
        )


def test_given_expires_at_in_past_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException, match=re.escape("expires_at cannot be in the past")
    ):
        ShortLinkAggregate.create_new(
            short_code="a1b2c3d",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
            is_custom=False,
        )


def test_given_expires_at_in_future_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape("expires_at cannot be more than 2 weeks from now"),
    ):
        ShortLinkAggregate.create_new(
            short_code="a1b2c3d",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=3),
            is_custom=False,
        )


def test_given_short_code_with_more_than_7_characters_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException, match=re.escape("short_code must be 7 characters long")
    ):
        ShortLinkAggregate.create_new(
            short_code="a1b2c3d4",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=False,
        )


def test_given_short_code_with_less_than_7_characters_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException, match=re.escape("short_code must be 7 characters long")
    ):
        ShortLinkAggregate.create_new(
            short_code="a1b2c3",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=False,
        )


def test_given_short_code_with_three_consecutive_characters_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape(
            "short_code must not repeat the same character three times in a row"
        ),
    ):
        ShortLinkAggregate.create_new(
            short_code="aaa1357",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=False,
        )


def test_given_short_code_with_special_characters_when_create_new_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape("short_code must be base62 (0-9, A-Z, a-z only)"),
    ):
        ShortLinkAggregate.create_new(
            short_code="a1b@c3d",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=False,
        )


def test_given_short_code_with_special_characters_when_create_new_and_is_custom_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape("custom short_code must be base63 (0-9, A-Z, a-z, - only)"),
    ):
        ShortLinkAggregate.create_new(
            short_code="my@brand",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=True,
        )


def test_given_short_code_with_first_character_not_in_base62_when_create_new_and_is_custom_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape("custom short_code must start with a base62 character"),
    ):
        ShortLinkAggregate.create_new(
            short_code="@my-brand",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=True,
        )


def test_given_short_code_with_last_character_not_in_base62_when_create_new_and_is_custom_then_should_raise_domain_exception():
    with pytest.raises(
        DomainException,
        match=re.escape("custom short_code must end with a base62 character"),
    ):
        ShortLinkAggregate.create_new(
            short_code="my-brand@",
            url="https://example.com",
            expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
            is_custom=True,
        )


def test_given_valid_inputs_when_create_from_datasource_then_should_instantiate_shortlink_aggregate():
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(days=1)
    aggregate = ShortLinkAggregate.create_from_datasource(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        created_at=created_at,
        expires_at=expires_at,
        is_custom=False,
    )
    assert aggregate.id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert aggregate.short_code == "a1b2c3d"
    assert aggregate.url == "https://example.com"
    assert aggregate.created_at == created_at
    assert aggregate.expires_at == expires_at
    assert aggregate.is_custom == False


def test_given_valid_inputs_when_create_from_datasource_and_is_custom_then_should_instantiate_shortlink_aggregate():
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(days=1)
    aggregate = ShortLinkAggregate.create_from_datasource(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        short_code="a1b2c3d",
        url="https://example.com",
        created_at=created_at,
        expires_at=expires_at,
        is_custom=True,
    )
    assert aggregate.id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert aggregate.short_code == "a1b2c3d"
    assert aggregate.url == "https://example.com"
    assert aggregate.created_at == created_at
    assert aggregate.expires_at == expires_at
    assert aggregate.is_custom == True
