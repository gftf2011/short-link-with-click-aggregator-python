from shared.domain.notification import Notification
from short_link.domain.validators.url.url_business_validation import (
    UrlBusinessValidation,
)
from short_link.domain.validators.url.url_empty_business_validation import (
    UrlEmptyBusinessValidation,
)
from short_link.domain.validators.url.url_valid_business_validation import (
    UrlValidBusinessValidation,
)


class UrlValidatorPipeline:
    @staticmethod
    def validate(url: str, notification: Notification):
        pipeline: list[UrlBusinessValidation] = [
            UrlEmptyBusinessValidation(),
            UrlValidBusinessValidation(),
        ]
        for validator in pipeline:
            validator.validate(url, notification)
            if validator.rejected:
                break
