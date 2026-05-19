from shared.constants.base_62 import BASE62
from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeBase62BusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if not all(char in BASE62 for char in short_code):
            notification.add_exception(
                DomainException("short_code must be base62 (0-9, A-Z, a-z only)")
            )
