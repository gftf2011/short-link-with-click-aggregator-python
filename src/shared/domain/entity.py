from uuid import UUID, uuid7
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from shared.domain.notification import Notification


@dataclass(eq=False, kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=lambda: uuid7())
    notification: Notification = field(default_factory=Notification, init=False)

    @abstractmethod
    def validate(self) -> None:
        pass
