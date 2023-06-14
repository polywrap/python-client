import json
from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_json_parse(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("json-type", implementation)
    value = { "foo": "bar", "bar": "bar" }
    json_value = json.dumps(value)

    response = client.invoke(
        uri=uri,
        method="parse",
        args={
            "value": json_value,
        },
    )

    assert json.loads(response) == value


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_json_stringify(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("json-type", implementation)
    values = [json.dumps({"bar": "foo"}), json.dumps({"foo": "bar"})]

    response = client.invoke(
        uri=uri,
        method="stringify",
        args={
            "values": values,
        },
    )

    # Note: python json.dumps() adds a space after the colon,
    #       but the JS implementation does not.
    assert response.replace(":", ": ") == "".join(values)
