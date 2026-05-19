from abc import ABC, abstractmethod
from datetime import datetime

from shared.domain.notification import Notification


class ExpiresAtBusinessValidation(ABC):
    rejected: bool = False

    @abstractmethod
    def validate(self, expires_at: datetime, notification: Notification) -> None:
        pass
