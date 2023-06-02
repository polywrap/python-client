from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri, WrapAbortError
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_required_enum(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("enum-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="method1",
            args={
                "en": 5,
            }
        )
    
    assert "Invalid value for enum 'SanityEnum': 5" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_valid_enum(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("enum-type", implementation)

    response = client.invoke(
        uri=uri,
        method="method1",
        args={
            "en": 2,
            "optEnum": 1,
        }
    )

    assert response == 2


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_invalid_optional_enum(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("enum-type", implementation)

    with pytest.raises(WrapAbortError) as err:
        client.invoke(
            uri=uri,
            method="method1",
            args={
                "en": 2,
                "optEnum": "INVALID",
            }
        )
    
    assert "Invalid key for enum 'SanityEnum': INVALID" in err.value.args[0]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_valid_enum_array(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("enum-type", implementation)

    response = client.invoke(
        uri=uri,
        method="method2",
        args={
            "enumArray": ["OPTION1", 0, "OPTION3"],
        }
    )

    assert response == [0, 0, 2]
