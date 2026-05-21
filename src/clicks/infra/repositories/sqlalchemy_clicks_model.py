from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.infra.models.base import Base


class SqlAlchemyClicksModel(Base):
    __tablename__ = "click"

    short_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
