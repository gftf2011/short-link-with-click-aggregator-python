from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import UUID

from shared.domain.entity import Entity
from shared.domain.exceptions import DomainException
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent
from short_link.domain.validators.expires_at.expires_at_validator_pipeline import (
    ExpiresAtValidatorPipeline as ExpiresAtValidator,
)
from short_link.domain.validators.short_code.short_code_validatior_pipeline import (
    ShortCodeValidatorPipeline as ShortCodeValidator,
)
from short_link.domain.validators.url.url_validator_pipeline import (
    UrlValidatorPipeline as UrlValidator,
)


@dataclass(eq=False, kw_only=True)
class ShortLinkAggregate(Entity):
    short_code: str
    url: str
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_custom: bool = field(default=False)

    @staticmethod
    def create_from_datasource(
        id: UUID,
        short_code: str,
        url: str,
        created_at: datetime,
        expires_at: datetime,
        is_custom: bool,
    ) -> "ShortLinkAggregate":
        aggregate = ShortLinkAggregate(
            id=id,
            short_code=short_code,
            url=url,
            created_at=created_at,
            expires_at=expires_at,
            is_custom=is_custom,
        )
        return aggregate

    @staticmethod
    def create_new(
        short_code: str,
        url: str,
        expires_at: datetime | None = None,
        is_custom: bool = False,
    ) -> "ShortLinkAggregate":
        aggregate = ShortLinkAggregate(
            short_code=short_code,
            url=url,
            expires_at=expires_at or (datetime.now(timezone.utc) + timedelta(weeks=2)),
            is_custom=is_custom,
        )
        aggregate.validate()
        return aggregate

    def validate(self):
        ShortCodeValidator.validate(self.short_code, self.is_custom, self.notification)
        UrlValidator.validate(self.url, self.notification)
        ExpiresAtValidator.validate(self.expires_at, self.notification)
        if self.notification.has_exceptions():
            raise DomainException(self.notification.messages)

    def validate_expires_at(self):
        ExpiresAtValidator.validate(self.expires_at, self.notification)
        if self.notification.has_exceptions():
            raise DomainException(self.notification.messages)

    def click(self) -> None:
        self.events.append(ShortlinkClickedEvent(short_code=self.short_code))
