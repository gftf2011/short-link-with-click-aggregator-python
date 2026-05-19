from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.url.url_business_validation import (
    UrlBusinessValidation,
)


class UrlEmptyBusinessValidation(UrlBusinessValidation):
    def validate(self, url: str, notification: Notification) -> None:
        if not url:
            notification.add_exception(DomainException("url cannot be empty"))
            self.rejected = True
