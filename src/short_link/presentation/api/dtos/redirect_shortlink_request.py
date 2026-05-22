from pydantic import BaseModel


class RedirectShortLinkRequestDTO(BaseModel):
    code: str
    click_impression_id: str
