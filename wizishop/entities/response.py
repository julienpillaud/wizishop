from pydantic import BaseModel


class WiziShopResponse(BaseModel):
    status_code: int
    content: str
