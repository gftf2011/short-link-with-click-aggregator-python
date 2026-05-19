from shared.domain.notification import Notification
from shared.domain.exceptions import DomainException
from shared.constants.base_62 import BASE62
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeCustomBase62LastCharacterBusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        if short_code[-1] not in BASE62:
            notification.add_exception(
                DomainException("custom short_code must end with a base62 character")
            )
