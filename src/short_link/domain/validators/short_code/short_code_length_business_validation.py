from shared.constants.length import LENGTH
from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeLengthBusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if len(short_code) != LENGTH:
            notification.add_exception(
                DomainException(f"short_code must be {LENGTH} characters long")
            )
