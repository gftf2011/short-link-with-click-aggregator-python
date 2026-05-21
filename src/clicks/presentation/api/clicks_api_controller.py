from shared.usecases.usecase import UseCase
from clicks.usecases.get_clicks_count_by_short_code.get_clicks_count_by_short_code_use_case import (
    GetClicksCountByShortCodeUseCaseInput,
    GetClicksCountByShortCodeUseCaseOutput,
)
from clicks.presentation.api.dtos.get_clicks_count_request import GetClicksCountRequestDTO
from clicks.presentation.api.dtos.get_clicks_count_response import (
    GetClicksCountFailureResponseDataDTO,
    GetClicksCountResponseDTO,
    GetClicksCountSuccessResponseDataDTO,
)


class ClicksApiController:
    def __init__(
        self,
        get_clicks_count_use_case: UseCase[
            GetClicksCountByShortCodeUseCaseInput,
            GetClicksCountByShortCodeUseCaseOutput,
        ],
    ) -> None:
        self.get_clicks_count_use_case = get_clicks_count_use_case

    async def get_clicks_count(
        self, request: GetClicksCountRequestDTO
    ) -> GetClicksCountResponseDTO:
        try:
            output = await self.get_clicks_count_use_case.execute(
                GetClicksCountByShortCodeUseCaseInput(short_code=request.short_code)
            )
            return GetClicksCountResponseDTO(
                status=200,
                data=GetClicksCountSuccessResponseDataDTO(
                    short_code=request.short_code,
                    count=output.count,
                ),
            )
        except Exception as e:
            return GetClicksCountResponseDTO(
                status=500,
                data=GetClicksCountFailureResponseDataDTO(error=str(e)),
            )
