import httpx
import pytest

from wizishop import WiziShopClient
from wizishop.entities.product import DEFAULT_PAGINATION_LIMIT, Product


@pytest.mark.asyncio
async def test_get_products(client: WiziShopClient) -> None:
    products = await client.get_products_async()

    assert products
    assert products.page == 1
    assert products.limit == DEFAULT_PAGINATION_LIMIT
    assert len(products.results) == DEFAULT_PAGINATION_LIMIT


@pytest.mark.asyncio
async def test_get_products_with_limit(client: WiziShopClient) -> None:
    products = await client.get_products_async(limit=1)

    assert products
    assert products.page == 1
    assert products.limit == 1
    assert len(products.results) == 1


@pytest.mark.asyncio
async def test_get_products_with_status(client: WiziShopClient) -> None:
    products = await client.get_products_async(status="visible")

    assert products
    assert products.page == 1
    assert products.limit == DEFAULT_PAGINATION_LIMIT
    assert len(products.results) == DEFAULT_PAGINATION_LIMIT
    assert all(product.status == "visible" for product in products.results)


@pytest.mark.asyncio
async def test_get_products_with_sku(client: WiziShopClient, product: Product) -> None:
    products = await client.get_products_async(sku=product.sku)

    assert products
    assert products.page == 1
    assert products.limit == DEFAULT_PAGINATION_LIMIT
    assert len(products.results) == 1
    assert products.results[0].sku == product.sku


@pytest.mark.asyncio
async def test_get_products_with_sort(client: WiziShopClient) -> None:
    products = await client.get_products_async(sort="id")

    assert products
    assert products.page == 1
    assert products.limit == DEFAULT_PAGINATION_LIMIT
    assert len(products.results) == DEFAULT_PAGINATION_LIMIT
    assert products.results[0].id < products.results[1].id


@pytest.mark.asyncio
async def test_update_sku_stock(client: WiziShopClient, product: Product) -> None:
    response = await client.update_sku_stock_async(
        sku=product.sku,
        stock=product.stock,  # type: ignore
    )

    assert response.status_code == httpx.codes.OK
    assert response.content == ""
