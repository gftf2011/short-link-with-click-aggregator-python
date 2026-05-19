from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/v1", tags=["health"])


@router.get("/health", status_code=200)
async def healthcheck() -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": "ok"})
