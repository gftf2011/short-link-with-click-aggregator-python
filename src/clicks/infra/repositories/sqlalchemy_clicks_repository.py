from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from clicks.domain.repositories.clicks_repository import ClicksRepository
from clicks.infra.repositories.sqlalchemy_clicks_model import SqlAlchemyClicksModel


class SqlAlchemyClicksRepository(ClicksRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def increment_clicks(self, counts: dict[str, int]) -> None:
        if not counts:
            return
        stmt = insert(SqlAlchemyClicksModel).values(
            [{"short_code": code, "count": count} for code, count in counts.items()]
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["short_code"],
            set_={"count": SqlAlchemyClicksModel.count + stmt.excluded.count},
        )
        await self.session.execute(stmt)
