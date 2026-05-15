from json import JSONDecodeError

import httpx

from wizishop.asynchronous import AsyncClient
from wizishop.exceptions import WiziShopError
from wizishop.synchronous import SyncClient


class WiziShopClient(SyncClient, AsyncClient):
    def __init__(self, username: str, password: str) -> None:
        try:
            response = httpx.post(
                f"{self.API_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=2,
            )
            response.raise_for_status()
            account = response.json()
            self._shop_id = account["default_shop_id"]
            self._headers = {"Authorization": f"Bearer {account['token']}"}
        except (httpx.HTTPError, JSONDecodeError, KeyError) as error:
            raise WiziShopError("Authentication failed") from error

        SyncClient.__init__(self, shop_id=self._shop_id, headers=self._headers)
        AsyncClient.__init__(self, shop_id=self._shop_id, headers=self._headers)
