from clicks.domain.gateways.clicks_gateway import ClicksGateway
from clicks.domain.lock.clicks_lock import ClicksLock
from clicks.domain.repositories.clicks_repository import ClicksRepository
from shared.handlers.handler import Handler


class FlushClicksHandler(Handler[None, None]):
    def __init__(
        self,
        gateway: ClicksGateway,
        repository: ClicksRepository,
        lock: ClicksLock,
    ) -> None:
        self.gateway = gateway
        self.repository = repository
        self.lock = lock

    async def handle(self, input: None) -> None:
        async with self.lock as lock:
            if not lock.acquired:
                return
            counts = await self.gateway.get_clicks_count()
            if not counts:
                return
            await self.repository.increment_clicks(counts)
            await self.gateway.reset_clicks_count()
