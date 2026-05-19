from abc import ABC, abstractmethod

from shared.domain.notification import Notification


class UrlBusinessValidation(ABC):
    rejected: bool = False

    @abstractmethod
    def validate(self, url: str, notification: Notification) -> None:
        pass
