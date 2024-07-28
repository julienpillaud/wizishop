import os

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel

from wizishop import WiziShopClient
from wizishop.entities.product import Product

load_dotenv()


class Authentication(BaseModel):
    username: str
    password: str


@pytest.fixture
def authentication() -> Authentication:
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    if username and password:
        return Authentication(username=username, password=password)

    raise ValueError("Missing authentication values")


@pytest.fixture
def client(authentication: Authentication) -> WiziShopClient:
    return WiziShopClient(authentication.username, authentication.password)


@pytest.fixture
def product(client: WiziShopClient) -> Product:
    products = client.get_products().results
    if product := next((product for product in products if product.stock), None):
        return product
    raise ValueError("No product with stock")
