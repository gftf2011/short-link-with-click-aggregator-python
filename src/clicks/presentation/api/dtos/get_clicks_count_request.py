from pydantic import BaseModel


class GetClicksCountRequestDTO(BaseModel):
    short_code: str
