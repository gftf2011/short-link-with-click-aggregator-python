from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, Text, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from shared.infra.models.base import Base


class SqlAlchemyShortLinkModel(Base):
    __tablename__ = "short_link"
    __table_args__ = (UniqueConstraint("short_code", "created_at"),)

    id: Mapped[UUID] = mapped_column(Uuid[UUID](as_uuid=True), primary_key=True)
    short_code: Mapped[str] = mapped_column(
        String(32), nullable=False, primary_key=True
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
