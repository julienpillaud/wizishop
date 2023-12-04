import os

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel

from wizishop import WiziShopClient

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
