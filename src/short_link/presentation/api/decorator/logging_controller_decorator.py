import json
import logging

from short_link.presentation.api.short_link_api_controller import ShortLinkApiController
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
)

logger = logging.getLogger(__name__)


class LoggingControllerDecorator(ShortLinkApiController):
    def __init__(self, controller: ShortLinkApiController):
        self.controller = controller

    async def create(
        self, request: CreateShortLinkRequestDTO
    ) -> CreateShortLinkResponseDTO:
        log_data: dict[str, str] = {}
        log_data["request"] = request.model_dump_json()
        data = await self.controller.create(request)
        log_data["response"] = data.model_dump_json()
        logger.info(json.dumps(log_data))
        return data

    async def redirect(
        self, request: RedirectShortLinkRequestDTO
    ) -> RedirectShortLinkResponseDTO:
        log_data: dict[str, str] = {}
        log_data["request"] = request.model_dump_json()
        data = await self.controller.redirect(request)
        log_data["response"] = data.model_dump_json()
        logger.info(json.dumps(log_data))
        return data
