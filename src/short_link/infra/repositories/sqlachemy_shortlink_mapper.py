from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.infra.repositories.sqlalchemy_shortlink_model import (
    SqlAlchemyShortLinkModel,
)


class SqlachemyShortLinkMapper:
    @staticmethod
    def to_model(short_link: ShortLinkAggregate) -> SqlAlchemyShortLinkModel:
        return SqlAlchemyShortLinkModel(
            id=short_link.id,
            short_code=short_link.short_code,
            url=short_link.url,
            expires_at=short_link.expires_at,
            created_at=short_link.created_at,
            is_custom=short_link.is_custom,
        )

    @staticmethod
    def to_aggregate(model: SqlAlchemyShortLinkModel) -> ShortLinkAggregate:
        return ShortLinkAggregate.create_from_datasource(
            id=model.id,
            short_code=model.short_code,
            url=model.url,
            created_at=model.created_at,
            expires_at=model.expires_at,
            is_custom=model.is_custom,
        )
