from wizishop import WiziShopClient


def test_get_products(client: WiziShopClient) -> None:
    products = client.get_products()

    assert products
    assert products.page == 1
    assert products.limit == 20
    assert len(products.results) == 20


def test_get_products_with_limit(client: WiziShopClient) -> None:
    products = client.get_products(limit=1)

    assert products
    assert products.page == 1
    assert products.limit == 1
    assert len(products.results) == 1


def test_get_products_with_status(client: WiziShopClient) -> None:
    products = client.get_products(status="visible")

    assert products
    assert products.page == 1
    assert products.limit == 20
    assert len(products.results) == 20
    assert all(product.status == "visible" for product in products.results)


def test_get_products_with_sku(client: WiziShopClient) -> None:
    sku = "5c0a297a6f22980815358aae"
    products = client.get_products(sku=sku)

    assert products
    assert products.page == 1
    assert products.limit == 20
    assert len(products.results) == 1
    assert products.results[0].sku == sku


def test_get_products_with_sort(client: WiziShopClient) -> None:
    products = client.get_products(sort="id")

    assert products
    assert products.page == 1
    assert products.limit == 20
    assert len(products.results) == 20
    assert products.results[0].id < products.results[1].id
