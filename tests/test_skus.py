import httpx

from wizishop import WiziShopClient
from wizishop.entities.product import Product


def test_update_sku_stock(client: WiziShopClient, product: Product) -> None:
    response = client.update_sku_stock(sku=product.sku, stock=product.stock)  # type: ignore

    assert response.status_code == httpx.codes.OK
    assert response.content == ""
