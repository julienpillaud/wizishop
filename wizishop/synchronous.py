from typing import Any

import httpx

from wizishop.entities.product import (
    DEFAULT_PAGINATION_LIMIT,
    ProductResponse,
    ProductStatus,
    SortableField,
)
from wizishop.entities.response import WiziShopResponse
from wizishop.entities.sku import UpdateStockMethod
from wizishop.exceptions import WiziShopError
from wizishop.mixin import WiziShopMixin


class SyncClient(WiziShopMixin):
    def __init__(self, shop_id: str, headers: dict[str, str]) -> None:
        self._shop_id = shop_id
        self._headers = headers

    def _request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> httpx.Response:
        try:
            with httpx.Client(headers=self._headers, timeout=2) as client:
                response = client.request(method, url, params=params, json=json)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise WiziShopError(str(error)) from error

        return response

    def get_products(
        self,
        limit: int = DEFAULT_PAGINATION_LIMIT,
        page: int = 1,
        status: ProductStatus | None = None,
        sku: str | None = None,
        sort: SortableField | None = None,
    ) -> ProductResponse:
        params = self._build_product_params(
            limit=limit,
            page=page,
            status=status,
            sku=sku,
            sort=sort,
        )
        response = self._request(
            method="GET",
            url=f"{self.API_URL}/shops/{self._shop_id}/products",
            params=params,
        )
        return self._handle_validation(
            response=response,
            response_model=ProductResponse,
        )

    def update_sku_stock(
        self,
        sku: str,
        stock: int,
        method: UpdateStockMethod = "replace",
    ) -> WiziShopResponse:
        response = self._request(
            method="PUT",
            url=f"{self.API_URL}/shops/{self._shop_id}/skus/{sku}",
            json={"method": method, "stock": stock},
        )
        return WiziShopResponse(
            status_code=response.status_code,
            content=response.text,
        )
