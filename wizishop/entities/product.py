from typing import Literal

from pydantic import BaseModel

DEFAULT_PAGINATION_LIMIT = 20

SortableField = Literal["id", "sku", "label", "stock", "weight"]
ProductStatus = Literal["draft", "scheduled", "visible", "hidden", "unavailable"]


class Product(BaseModel):
    id: str
    sku: str
    label: str
    stock: int | None
    weight: float
    image_url: str | None
    status: ProductStatus


class ProductResponse(BaseModel):
    page: int
    limit: int
    pages: int
    total: int
    results: list[Product]
