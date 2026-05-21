from pydantic import BaseModel


class GetClicksCountSuccessResponseDataDTO(BaseModel):
    short_code: str
    count: int


class GetClicksCountFailureResponseDataDTO(BaseModel):
    error: str


class GetClicksCountResponseDTO(BaseModel):
    status: int
    data: GetClicksCountSuccessResponseDataDTO | GetClicksCountFailureResponseDataDTO
