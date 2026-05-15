import pytest

from wizishop import WiziShopClient, WiziShopError


def test_client_bad_credentials() -> None:
    with pytest.raises(WiziShopError) as error:
        WiziShopClient(username="username", password="password")

    assert str(error.value) == "Authentication failed"
