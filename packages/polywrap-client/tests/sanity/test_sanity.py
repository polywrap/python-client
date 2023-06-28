from typing import Callable, Any
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_sanity(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
    capsys: Any
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bytes-type", implementation)

    prop = b"hello world"
    expected = b"hello world Sanity!"

    response: bytes = client.invoke(
        uri=uri,
        method="bytesMethod",
        args={
            "arg": {
                "prop": prop,
            }
        },
    )

    assert response == expected

    # Make sure nothing was printed to stdout or stderr
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
