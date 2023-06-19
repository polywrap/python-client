from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_bignumber_method_with_arg1_and_obj(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bignumber-type", implementation)

    arg1 = "1234.56789123456789"
    prop1 = "98.7654321987654321"

    response = client.invoke(
        uri=uri,
        method="method",
        args={
            "arg1": arg1,
            "obj": {
                "prop1": prop1,
            },
        },
    )

    import decimal
    decimal.getcontext().prec = len(response)

    arg1 = decimal.Decimal(arg1)
    prop1 = decimal.Decimal(prop1)
    result = arg1 * prop1


    assert response == str(result)


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_bignumber_method_with_arg1_arg2_and_obj(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bignumber-type", implementation)

    arg1 = "1234567.89123456789"
    arg2 = "123456789123.456789123456789123456789"
    prop1 = "987654.321987654321"
    prop2 = "987.654321987654321987654321987654321"

    response = client.invoke(
        uri=uri,
        method="method",
        args={
            "arg1": arg1,
            "arg2": arg2,
            "obj": {
                "prop1": prop1,
                "prop2": prop2,
            },
        },
    )

    import decimal

    decimal.getcontext().prec = len(response)

    arg1 = decimal.Decimal(arg1)
    arg2 = decimal.Decimal(arg2)
    prop1 = decimal.Decimal(prop1)
    prop2 = decimal.Decimal(prop2)
    result = arg1 * arg2 * prop1 * prop2

    assert response == str(result)
