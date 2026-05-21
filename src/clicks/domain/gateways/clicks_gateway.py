from abc import ABC


class ClicksGateway(ABC):
    async def get_clicks_count(self) -> dict[str, int]:
        raise NotImplementedError

    async def reset_clicks_count(self) -> None:
        raise NotImplementedError
