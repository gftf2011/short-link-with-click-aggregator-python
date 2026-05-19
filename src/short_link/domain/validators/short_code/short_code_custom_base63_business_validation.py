from shared.constants.base_63 import BASE63
from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeCustomBase63BusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if not all(char in BASE63 for char in short_code):
            notification.add_exception(
                DomainException(
                    "custom short_code must be base63 (0-9, A-Z, a-z, - only)"
                )
            )
