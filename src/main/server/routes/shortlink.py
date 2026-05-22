import hashlib
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.server.configs.asyncsession import get_async_session
from short_link.main.factory.shortlink import http
from short_link.presentation.api.dtos.create_shortlink_request import (
    CreateShortLinkRequestDTO,
)
from short_link.presentation.api.dtos.create_shortlink_response import (
    CreateShortLinkResponseDTO,
)
from short_link.presentation.api.dtos.redirect_shortlink_request import (
    RedirectShortLinkRequestDTO,
)
from short_link.presentation.api.dtos.redirect_shortlink_response import (
    RedirectShortLinkResponseDTO,
    RedirectShortLinkSuccessResponseDataDTO,
)

router = APIRouter(prefix="/v1", tags=["shortlink"])


def impression_id(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    ip = (
        forwarded_for.split(",")[0].strip()
        if forwarded_for
        else (request.client.host if request.client else "unknown")
    )
    code = request.path_params.get("code", "")
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return hashlib.sha256(f"{code}:{ip}:{timestamp}".encode()).hexdigest()


@router.post(
    "/shortlink",
    response_model=CreateShortLinkResponseDTO,
    responses={
        201: {"description": "Created", "model": CreateShortLinkResponseDTO},
        400: {"description": "Validation error", "model": CreateShortLinkResponseDTO},
    },
)
async def create_shortlink(
    request: CreateShortLinkRequestDTO,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> JSONResponse:
    shortlink_controller = http(session)
    result = await shortlink_controller.create(request)
    return JSONResponse(
        status_code=result.status,
        content=result.model_dump(mode="json"),
    )


@router.get(
    "/shortlink/{code}",
    response_model=None,
    responses={
        302: {"description": "Redirect to the stored URL (Location header)"},
        400: {"description": "Validation error", "model": RedirectShortLinkResponseDTO},
        404: {
            "description": "Short link not found",
            "model": RedirectShortLinkResponseDTO,
        },
    },
)
async def redirect_shortlink(
    code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    click_impression_id: Annotated[str, Depends(impression_id)],
) -> RedirectResponse | JSONResponse:
    shortlink_controller = http(session)
    result = await shortlink_controller.redirect(RedirectShortLinkRequestDTO(code=code, click_impression_id=click_impression_id))
    if result.status == 302 and isinstance(
        result.data, RedirectShortLinkSuccessResponseDataDTO
    ):
        return RedirectResponse(url=result.data.url, status_code=302)
    return JSONResponse(
        status_code=result.status,
        content=result.model_dump(mode="json"),
    )
