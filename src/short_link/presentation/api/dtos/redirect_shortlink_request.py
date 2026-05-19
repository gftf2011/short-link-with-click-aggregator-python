from pydantic import BaseModel


class RedirectShortLinkRequestDTO(BaseModel):
    code: str
