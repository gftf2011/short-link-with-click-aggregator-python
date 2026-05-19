from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeCustomLengthBusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if len(short_code) > 32:
            notification.add_exception(
                DomainException(
                    f"custom short_code must be less than 32 characters long"
                )
            )
