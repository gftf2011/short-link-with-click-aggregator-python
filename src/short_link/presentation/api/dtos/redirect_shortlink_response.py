from pydantic import BaseModel


class RedirectShortLinkSuccessResponseDataDTO(BaseModel):
    url: str


class RedirectShortLinkFailureResponseDataDTO(BaseModel):
    error: str


class RedirectShortLinkResponseDTO(BaseModel):
    status: int
    data: (
        RedirectShortLinkSuccessResponseDataDTO
        | RedirectShortLinkFailureResponseDataDTO
    )
