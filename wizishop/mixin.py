from json import JSONDecodeError
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from wizishop.entities.product import (
    DEFAULT_PAGINATION_LIMIT,
    ProductStatus,
    SortableField,
)
from wizishop.exceptions import WiziShopError


class WiziShopMixin:
    API_URL = "https://api.wizishop.com/v3"

    @staticmethod
    def _build_product_params(
        limit: int = DEFAULT_PAGINATION_LIMIT,
        page: int = 1,
        status: ProductStatus | None = None,
        sku: str | None = None,
        sort: SortableField | None = None,
    ) -> dict[str, Any]:
        params = {
            "limit": limit,
            "page": page,
            "status": status,
            "sku": sku,
            "sort": sort,
        }
        return {key: value for key, value in params.items() if value is not None}

    @staticmethod
    def _handle_validation[T: BaseModel](
        response: httpx.Response,
        response_model: type[T],
    ) -> T:
        try:
            result = response.json()
            return response_model.model_validate(result)
        except (JSONDecodeError, ValidationError) as error:
            raise WiziShopError(str(error)) from error
