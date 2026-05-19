from datetime import datetime

from shared.domain.notification import Notification
from short_link.domain.validators.expires_at.expires_at_business_validation import (
    ExpiresAtBusinessValidation,
)
from short_link.domain.validators.expires_at.expires_at_in_future_business_validation import (
    ExpiresAtValidatorInTheFutureValidator,
)
from short_link.domain.validators.expires_at.expires_at_in_past_business_validation import (
    ExpiresAtValidatorInThePastValidator,
)


class ExpiresAtValidatorPipeline:
    @staticmethod
    def validate(expires_at: datetime, notification: Notification):
        pipeline: list[ExpiresAtBusinessValidation] = [
            ExpiresAtValidatorInThePastValidator(),
            ExpiresAtValidatorInTheFutureValidator(),
        ]
        for validator in pipeline:
            validator.validate(expires_at, notification)
            if validator.rejected:
                break
