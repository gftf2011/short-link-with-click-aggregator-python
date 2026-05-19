from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.infra.repositories.sqlachemy_shortlink_mapper import (
    SqlachemyShortLinkMapper,
)
from short_link.infra.repositories.sqlalchemy_shortlink_model import (
    SqlAlchemyShortLinkModel,
)


class SqlAlchemyShortLinkRepository(ShortLinkRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> ShortLinkAggregate | None:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=30)
        result = await self.session.execute(
            select(SqlAlchemyShortLinkModel)
            .where(SqlAlchemyShortLinkModel.short_code == code)
            .where(SqlAlchemyShortLinkModel.created_at >= start_time)
            .where(SqlAlchemyShortLinkModel.created_at < end_time)
            .order_by(SqlAlchemyShortLinkModel.created_at.desc())
            .limit(1)
        )

        model: SqlAlchemyShortLinkModel | None = result.scalars().first()
        if model is None:
            return None
        return SqlachemyShortLinkMapper.to_aggregate(model)

    def create(self, short_link: ShortLinkAggregate) -> None:
        self.session.add(SqlachemyShortLinkMapper.to_model(short_link))
