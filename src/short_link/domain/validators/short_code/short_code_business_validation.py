from abc import ABC, abstractmethod

from shared.domain.notification import Notification


class ShortCodeBusinessValidation(ABC):
    rejected: bool = False

    @abstractmethod
    def validate(self, short_code: str, notification: Notification) -> None:
        pass
