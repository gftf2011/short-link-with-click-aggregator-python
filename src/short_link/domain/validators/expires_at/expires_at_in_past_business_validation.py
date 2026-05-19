from datetime import datetime, timezone

from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.expires_at.expires_at_business_validation import (
    ExpiresAtBusinessValidation,
)


class ExpiresAtValidatorInThePastValidator(ExpiresAtBusinessValidation):
    def validate(self, expires_at: datetime, notification: Notification) -> None:
        if expires_at < datetime.now(timezone.utc):
            notification.add_exception(
                DomainException("expires_at cannot be in the past")
            )
            self.rejected = True
