from pydantic import ValidationError
from shared.domain.exceptions import DomainException
from shared.usecases.exceptions import ApplicationException
from shared.usecases.usecase import UseCase
from short_link.usecases.create_shortlink.create_shortlink_use_case import (
    CreateShortLinkUseCaseInput,
    CreateShortLinkUseCaseOutput,
)
from short_link.usecases.redirect_shortlink.redirect_shortlink_use_case import (
    RedirectShortLinkUseCaseInput,
    RedirectShortLinkUseCaseOutput,
)
from short_link.presentation.api.dtos.create_shortlink_request import (
    CreateShortLinkRequestDTO,
)
from short_link.presentation.api.dtos.create_shortlink_response import (
    CreateShortLinkFailureResponseDataDTO,
    CreateShortLinkResponseDTO,
    CreateShortLinkSuccessResponseDataDTO,
)
from short_link.presentation.api.dtos.redirect_shortlink_request import (
    RedirectShortLinkRequestDTO,
)
from short_link.presentation.api.dtos.redirect_shortlink_response import (
    RedirectShortLinkFailureResponseDataDTO,
    RedirectShortLinkResponseDTO,
    RedirectShortLinkSuccessResponseDataDTO,
)


class ApiController:
    @staticmethod
    def _status_for_exception(e: Exception, *, default: int) -> int:
        if isinstance(
            e, (DomainException, ValidationError)  # pyright: ignore[reportArgumentType]
        ):
            return 400
        if isinstance(e, ApplicationException):
            return 404
        return default

    def __init__(
        self,
        createShortLinkUseCase: UseCase[
            CreateShortLinkUseCaseInput, CreateShortLinkUseCaseOutput
        ],
        redirectShortLinkUseCase: UseCase[
            RedirectShortLinkUseCaseInput, RedirectShortLinkUseCaseOutput
        ],
    ):
        self.createShortLinkUseCase = createShortLinkUseCase
        self.redirectShortLinkUseCase = redirectShortLinkUseCase

    async def create(
        self, request: CreateShortLinkRequestDTO
    ) -> CreateShortLinkResponseDTO:
        usecase_input = CreateShortLinkUseCaseInput(
            url=request.url, expires_at=request.expires_at, alias=request.alias
        )
        try:
            output = await self.createShortLinkUseCase.execute(usecase_input)
            return CreateShortLinkResponseDTO(
                status=201,
                data=CreateShortLinkSuccessResponseDataDTO(code=output.code),
            )
        except Exception as e:
            status = self._status_for_exception(e, default=500)
            return CreateShortLinkResponseDTO(
                status=status,
                data=CreateShortLinkFailureResponseDataDTO(error=str(e)),
            )

    async def redirect(
        self, request: RedirectShortLinkRequestDTO
    ) -> RedirectShortLinkResponseDTO:
        usecase_input = RedirectShortLinkUseCaseInput(code=request.code)
        try:
            output = await self.redirectShortLinkUseCase.execute(usecase_input)
            return RedirectShortLinkResponseDTO(
                status=302,
                data=RedirectShortLinkSuccessResponseDataDTO(url=output.url),
            )
        except Exception as e:
            status = self._status_for_exception(e, default=500)
            return RedirectShortLinkResponseDTO(
                status=status,
                data=RedirectShortLinkFailureResponseDataDTO(error=str(e)),
            )
