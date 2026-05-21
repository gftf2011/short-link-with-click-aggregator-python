from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from clicks.main.factory.clicks import http
from clicks.presentation.api.dtos.get_clicks_count_request import GetClicksCountRequestDTO
from clicks.presentation.api.dtos.get_clicks_count_response import GetClicksCountResponseDTO
from main.server.configs.asyncsession import get_async_session

router = APIRouter(prefix="/v1", tags=["clicks"])


@router.get(
    "/clicks/{code}",
    response_model=GetClicksCountResponseDTO,
    responses={
        200: {"description": "Click count for the short code"},
    },
)
async def get_clicks_count(
    code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> JSONResponse:
    controller = http(session)
    result = await controller.get_clicks_count(GetClicksCountRequestDTO(short_code=code))
    return JSONResponse(status_code=result.status, content=result.model_dump(mode="json"))
