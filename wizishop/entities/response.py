from typing import Any

from pydantic import BaseModel


class WiziShopResponse(BaseModel):
    status_code: int
    content: str


class WiziShopErrorResponse(BaseModel):
    message: str
    code: int
    errors: Any
