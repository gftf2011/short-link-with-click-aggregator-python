from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeEmptyBusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if not short_code:
            notification.add_exception(DomainException("short_code cannot be empty"))
            self.rejected = True
