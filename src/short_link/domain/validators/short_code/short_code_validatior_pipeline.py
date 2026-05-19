from shared.domain.notification import Notification
from short_link.domain.validators.short_code.short_code_business_validation import (
    ShortCodeBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_custom_base62_first_character_business_validation import (
    ShortCodeCustomBase62FirstCharacterBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_custom_base62_last_character_business_validation import (
    ShortCodeCustomBase62LastCharacterBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_custom_base63_business_validation import (
    ShortCodeCustomBase63BusinessValidation,
)
from short_link.domain.validators.short_code.short_code_custom_length_business_validation import (
    ShortCodeCustomLengthBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_empty_business_validation import (
    ShortCodeEmptyBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_length_business_validation import (
    ShortCodeLengthBusinessValidation,
)
from short_link.domain.validators.short_code.short_code_base62_business_validation import (
    ShortCodeBase62BusinessValidation,
)
from short_link.domain.validators.short_code.short_code_repeat_business_validation import (
    ShortCodeRepeatBusinessValidation,
)


class ShortCodeValidatorPipeline:
    @staticmethod
    def validate(short_code: str, is_custom: bool, notification: Notification):
        pipeline: list[ShortCodeBusinessValidation] = []
        if is_custom:
            pipeline.extend(
                [
                    ShortCodeEmptyBusinessValidation(),
                    ShortCodeCustomLengthBusinessValidation(),
                    ShortCodeCustomBase62FirstCharacterBusinessValidation(),
                    ShortCodeCustomBase62LastCharacterBusinessValidation(),
                    ShortCodeCustomBase63BusinessValidation(),
                ]
            )
            for validator in pipeline:
                validator.validate(short_code, notification)
                if validator.rejected:
                    break
        else:
            pipeline.extend(
                [
                    ShortCodeEmptyBusinessValidation(),
                    ShortCodeLengthBusinessValidation(),
                    ShortCodeBase62BusinessValidation(),
                    ShortCodeRepeatBusinessValidation(),
                ]
            )
            for validator in pipeline:
                validator.validate(short_code, notification)
                if validator.rejected:
                    break
