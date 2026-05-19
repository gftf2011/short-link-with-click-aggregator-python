import os
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_connection_manager import SqlalchemyConnectionManager
from shared.usecases.decorators.retrieve_unitofwork import RetrieveUnitOfWork
from shared.usecases.decorators.transaction_unitofwork import TransactionUnitOfWork
from short_link.infra.gateways.redis_shortlink_gateway import RedisShortLinkGateway
from short_link.infra.repositories.proxy.redis_shortlink_repository import (
    RedisShortLinkRepositoryProxy,
)
from short_link.infra.repositories.sqlalchemy_shortlink_repository import (
    SqlAlchemyShortLinkRepository,
)
from short_link.presentation.batch.controller import BatchController
from short_link.presentation.api.controller import ApiController
from short_link.presentation.api.decorator.logging_controller_decorator import (
    LoggingControllerDecorator,
)
from short_link.usecases.batch_generate_shortlink_code.batch_generate_shortlink_code_use_case import (
    BatchGenerateShortlinkCodeUseCase,
)
from short_link.usecases.batch_generate_shortlink_code.decorator.logging_use_case import (
    LoggingBatchGenerateShortlinkCodeUseCase,
)
from short_link.usecases.create_shortlink.create_shortlink_use_case import (
    CreateShortLinkUseCase,
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)
from short_link.usecases.get_shortlink_code_counter.get_shortlink_code_counter_use_case import (
    GetShortlinkCodeCounterUseCase,
)
from short_link.usecases.redirect_shortlink.redirect_shortlink_use_case import (
    RedirectShortLinkUseCase,
    RedirectShortLinkUseCaseInput,
    RedirectShortLinkUseCaseOutput,
)
from short_link.usecases.set_shortlink_codes_and_counter.set_shortlink_codes_and_counter_use_case import (
    SetShortlinkCodesAndCounterUseCase,
)


def http(session: AsyncSession):
    from shared.infra.redis_database import (
        redis_client_for_shortlink_cache,
        redis_client_for_shortlink_codes,
    )

    connection_manager = SqlalchemyConnectionManager(session=session)

    short_link_repository = SqlAlchemyShortLinkRepository(session=session)
    short_link_repository_proxy = RedisShortLinkRepositoryProxy(
        short_link_repository=short_link_repository,
        redis=redis_client_for_shortlink_cache(),
    )
    shortlink_gateway = RedisShortLinkGateway(redis=redis_client_for_shortlink_codes())

    create_short_link_use_case = CreateShortLinkUseCase(
        short_link_repository=short_link_repository_proxy,
        shortlink_gateway=shortlink_gateway,
    )

    transaction_unitofwork = TransactionUnitOfWork[
        CreateShortLinkUseCaseInput, CreateShortLinkUseCaseOutput
    ](
        usecase=create_short_link_use_case,
        connection_manager=connection_manager,
    )

    redirect_short_link_use_case = RedirectShortLinkUseCase(
        short_link_repository=short_link_repository_proxy,
    )

    retrieve_unitofwork = RetrieveUnitOfWork[
        RedirectShortLinkUseCaseInput, RedirectShortLinkUseCaseOutput
    ](
        usecase=redirect_short_link_use_case,
        connection_manager=connection_manager,
    )

    controller = LoggingControllerDecorator(
        controller=ApiController(
            createShortLinkUseCase=transaction_unitofwork,
            redirectShortLinkUseCase=retrieve_unitofwork,
        )
    )

    return controller


def batch():
    from shared.infra.redis_database import redis_client_for_shortlink_codes

    shortlink_gateway = RedisShortLinkGateway(redis=redis_client_for_shortlink_codes())

    batch_generate_shortlink_code_use_case = LoggingBatchGenerateShortlinkCodeUseCase(
        batch_generate_shortlink_code_use_case=BatchGenerateShortlinkCodeUseCase(
            shortlink_gateway=shortlink_gateway,
        )
    )

    set_shortlink_codes_and_counter_use_case = SetShortlinkCodesAndCounterUseCase(
        shortlink_gateway=shortlink_gateway,
    )

    get_shortlink_code_counter_use_case = GetShortlinkCodeCounterUseCase(
        shortlink_gateway=shortlink_gateway,
    )

    batch_controller = BatchController(
        max=int(os.getenv("MAX_SHORTLINK_CODES") or "10_000"),
        chunk_size=int(os.getenv("SHORTLINK_CODES_BATCH_SIZE") or "100"),
        set_shortlink_codes_and_counter_use_case=set_shortlink_codes_and_counter_use_case,
        get_shortlink_code_counter_use_case=get_shortlink_code_counter_use_case,
        batch_generate_shortlink_code_use_case=batch_generate_shortlink_code_use_case,
    )

    return batch_controller
