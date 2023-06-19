from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_object_method1(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("object-type", implementation)
    obj = {
        "arg1": {
            "prop": "arg1 prop",
            "nested": {
                "prop": "arg1 nested prop",
            },
        }
    }

    response = client.invoke(
        uri=uri,
        method="method1",
        args=obj,
    )

    assert response == [obj["arg1"], {
        "prop": "",
        "nested": {
            "prop": "",
        },
    }]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_object_method2(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("object-type", implementation)
    obj = {
        "arg": {
            "prop": "null",
            "nested": {
                "prop": "arg nested prop",
            },
        }
    }

    response = client.invoke(
        uri=uri,
        method="method2",
        args=obj,
    )

    assert response is None


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_object_method3(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("object-type", implementation)
    obj = {
        "arg": {
            "prop": "arg prop",
            "nested": {
                "prop": "arg nested prop",
            },
        }
    }

    response = client.invoke(
        uri=uri,
        method="method3",
        args=obj,
    )

    assert response == [None, obj["arg"]]


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_object_method4(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("object-type", implementation)
    obj = {
        "arg": {
            "prop": [49, 50, 51, 52],
        }
    }

    response = client.invoke(
        uri=uri,
        method="method4",
        args=obj,
    )

    assert response == {
        "prop": "1234",
        "nested": {
            "prop": "nested prop",
        },
    }
