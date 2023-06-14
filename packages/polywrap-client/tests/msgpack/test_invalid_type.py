from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri, WrapAbortError
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_bool(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("invalid-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="boolMethod",
            args={"arg": 10},
        )

    assert "Property must be of type 'bool'. Found 'int'." in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_int(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("invalid-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="intMethod",
            args={"arg": "10"},
        )

    assert "Property must be of type 'int'. Found 'string'." in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_bytes(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("invalid-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="bytesMethod",
            args={"arg": 10.23},
        )

    assert "Property must be of type 'bytes'. Found 'float64'." in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_array(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("invalid-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="arrayMethod",
            args={"arg": {"prop": 1}},
        )

    assert "Property must be of type 'array'. Found 'map'." in err.value.args[0]
