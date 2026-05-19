import validators

from shared.domain.exceptions import DomainException
from shared.domain.notification import Notification
from short_link.domain.validators.url.url_business_validation import (
    UrlBusinessValidation,
)


class UrlValidBusinessValidation(UrlBusinessValidation):
    def validate(self, url: str, notification: Notification) -> None:
        if not validators.url(url):
            notification.add_exception(DomainException("url is not a valid URL"))
