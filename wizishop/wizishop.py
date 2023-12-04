from typing import Any

import httpx

from wizishop.entities.product import ProductResponse, ProductStatus, SortableField
from wizishop.entities.response import WiziShopResponse
from wizishop.entities.sku import UpdateStockMethod

API_URL = "https://api.wizishop.com/v3"


class WiziShopError(Exception):
    pass


class WiziShopClient:
    def __init__(self, username: str, password: str) -> None:
        url = f"{API_URL}/auth/login"
        data = {"username": username, "password": password}

        with httpx.Client(timeout=10) as client:
            response = client.post(url, json=data)

        if response.status_code != httpx.codes.CREATED:
            raise WiziShopError

        account = response.json()
        token = account["token"]
        self.headers = {"Authorization": f"Bearer {token}"}
        self.shop_id = account["default_shop_id"]

    def _request(
        self,
        method: str,
        url: str,
        expected_status: httpx.codes,
        params: Any = None,
        json: Any = None,
    ) -> Any:
        with httpx.Client(headers=self.headers, timeout=10) as client:
            response = client.request(method=method, url=url, params=params, json=json)

        if response.status_code != expected_status:
            raise WiziShopError

        return response

    def get_products(
        self,
        limit: int = 20,
        page: int = 1,
        status: ProductStatus | None = None,
        sku: str | None = None,
        sort: SortableField | None = None,
    ) -> ProductResponse:
        """Get products based on the given filters

        :param limit: Resources per page
        :param page: Page number
        :param status: Filter by status
        :param sku: Filter by SKU
        :param sort: Sort by field
        """
        url = f"{API_URL}/shops/{self.shop_id}/products"
        params: dict[str, Any] = {"limit": limit, "page": page}
        if status:
            params["status"] = status
        if sku:
            params["sku"] = sku
        if sort:
            params["sort"] = sort

        response = self._request(
            method="GET", url=url, expected_status=httpx.codes.OK, params=params
        )
        result = response.json()
        return ProductResponse.model_validate(result)

    def update_sku_stock(
        self, sku: str, stock: int, method: UpdateStockMethod = "replace"
    ):
        """Update stock for a given SKU

        :param sku: Stock-keeping unit
        :param stock: Stock quantity
        :param method: Update stock method
        """
        url = f"{API_URL}/shops/{self.shop_id}/skus/{sku}"
        json = {"method": method, "stock": stock}

        response = self._request(
            method="PUT", url=url, expected_status=httpx.codes.OK, json=json
        )
        return WiziShopResponse(status_code=response.status_code, content=response.text)
