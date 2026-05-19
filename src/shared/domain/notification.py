from dataclasses import dataclass, field


@dataclass
class Notification:
    exceptions: list[Exception] = field(default_factory=list)

    @property
    def messages(self) -> str:
        return "\n".join(str(exc) for exc in self.exceptions)

    def add_exception(self, exception: Exception) -> None:
        self.exceptions.append(exception)

    def has_exceptions(self) -> bool:
        return len(self.exceptions) > 0

    def get_exceptions(self) -> list[Exception]:
        return self.exceptions

    def clear_exceptions(self) -> None:
        self.exceptions = []
