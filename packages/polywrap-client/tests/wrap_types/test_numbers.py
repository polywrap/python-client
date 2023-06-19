from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri, WrapAbortError
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_int8(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="i8Method",
            args={
                "first": -129,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = -129; bits = 8" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_uint8(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="u8Method",
            args={
                "first": 256,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = 256; bits = 8" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_int16(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="i16Method",
            args={
                "first": -32769,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = -32769; bits = 16" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_uint16(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="u16Method",
            args={
                "first": 65536,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = 65536; bits = 16" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_int32(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="i32Method",
            args={
                "first": -2147483649,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = -2147483649; bits = 32" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_uint32(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("numbers-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="u32Method",
            args={
                "first": 4294967296,
                "second": 10,
            }
        )
    
    assert "integer overflow: value = 4294967296; bits = 32" in err.value.args[0]
