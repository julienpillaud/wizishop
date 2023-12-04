from typing import Literal

from pydantic import BaseModel

ProductStatus = Literal["draft", "scheduled", "visible", "hidden", "unavailable"]
SortableField = Literal["id", "sku", "label", "stock", "weight"]


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
