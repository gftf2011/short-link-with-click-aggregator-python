from shared.infra.redis_database import sync_redis_client_for_clicks


def load() -> None:
    sync_redis_client_for_clicks().ping()
