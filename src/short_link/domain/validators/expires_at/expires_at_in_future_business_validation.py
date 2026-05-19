from datetime import datetime, timezone, timedelta

from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.expires_at.expires_at_business_validation import (
    ExpiresAtBusinessValidation,
)


class ExpiresAtValidatorInTheFutureValidator(ExpiresAtBusinessValidation):
    def validate(self, expires_at: datetime, notification: Notification) -> None:
        if expires_at > datetime.now(timezone.utc) + timedelta(weeks=2):
            notification.add_exception(
                DomainException("expires_at cannot be more than 2 weeks from now")
            )
            self.rejected = True
