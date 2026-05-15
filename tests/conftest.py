import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict

from wizishop import WiziShopClient
from wizishop.entities.product import Product


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    username: str
    password: str


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()  # ty: ignore[missing-argument]


@pytest.fixture(scope="session")
def client(settings: Settings) -> WiziShopClient:
    return WiziShopClient(settings.username, settings.password)


@pytest.fixture
def product(client: WiziShopClient) -> Product:
    products = client.get_products(status="visible").results
    if not products:
        raise RuntimeError()

    product = products[0]
    if not product.stock:
        raise RuntimeError()

    return product
