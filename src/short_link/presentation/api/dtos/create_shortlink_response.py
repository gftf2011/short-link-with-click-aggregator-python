from pydantic import BaseModel


class CreateShortLinkSuccessResponseDataDTO(BaseModel):
    code: str


class CreateShortLinkFailureResponseDataDTO(BaseModel):
    error: str


class CreateShortLinkResponseDTO(BaseModel):
    status: int
    data: CreateShortLinkSuccessResponseDataDTO | CreateShortLinkFailureResponseDataDTO
