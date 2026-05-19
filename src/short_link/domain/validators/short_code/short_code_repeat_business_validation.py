from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)


class ShortCodeRepeatBusinessValidation(ShortCodeBusinessValidation):
    def validate(self, short_code: str, notification: Notification) -> None:
        for i in range(len(short_code) - 2):
            if short_code[i] == short_code[i + 1] == short_code[i + 2]:
                notification.add_exception(
                    DomainException(
                        "short_code must not repeat the same character three times in a row"
                    )
                )
