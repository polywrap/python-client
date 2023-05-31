from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_bigint_method_with_arg1_and_obj(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bigint-type", implementation)

    arg1 = "123456789123456789"
    prop1 = "987654321987654321"

    response = client.invoke(
        uri=uri, method="method", args={"arg1": arg1, "obj": {"prop1": prop1}}
    )

    result = int(arg1) * int(prop1)
    assert response == str(result)


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_bigint_method_with_arg1_arg2_and_obj(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bigint-type", implementation)

    arg1 = "123456789123456789"
    arg2 = "123456789123456789123456789123456789"
    prop1 = "987654321987654321"
    prop2 = "987654321987654321987654321987654321"

    response = client.invoke(
        uri=uri,
        method="method",
        args={"arg1": arg1, "arg2": arg2, "obj": {"prop1": prop1, "prop2": prop2}},
    )

    result = int(arg1) * int(arg2) * int(prop1) * int(prop2)
    assert response == str(result)
