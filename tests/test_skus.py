import httpx

from wizishop import WiziShopClient


def test_update_sku_stock(client: WiziShopClient) -> None:
    response = client.update_sku_stock(sku="5c0a297a6f22980815358aae", stock=0)

    assert response.status_code == httpx.codes.OK
    assert response.content == ""
