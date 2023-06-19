from typing import Callable, Dict
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ...consts import SUPPORTED_IMPLEMENTATIONS

@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_subsequent_invokes(implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]):
    client = PolywrapClient(builder.build())
    subsequent_invokes = client.invoke(
        uri=wrapper_uri(implementation),
        method="subsequentInvokes",
        args={
            "numberOfTimes": 40,
        },
    )

    expected = [str(index) for index in range(40)]
    assert subsequent_invokes == expected


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_local_var_method(implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]):
    client = PolywrapClient(builder.build())
    localVarMethod = client.invoke(
        uri=wrapper_uri(implementation),
        method="localVarMethod",
    )

    assert localVarMethod == True


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_global_var_method(implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]):
    client = PolywrapClient(builder.build())
    globalVarMethod = client.invoke(
        uri=wrapper_uri(implementation),
        method="globalVarMethod",
    )

    assert globalVarMethod == True


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_set_data_with_large_args(implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]):
    client = PolywrapClient(builder.build())
    large_str = "polywrap " * 10000

    setDataWithLargeArgs = client.invoke(
        uri=wrapper_uri(implementation),
        method="setDataWithLargeArgs",
        args={
            "value": large_str,
        },
    )

    assert setDataWithLargeArgs == large_str



@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_set_data_with_many_args(implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]):
    client = PolywrapClient(builder.build())
    args = {
        "valueA": "polywrap a",
        "valueB": "polywrap b",
        "valueC": "polywrap c",
        "valueD": "polywrap d",
        "valueE": "polywrap e",
        "valueF": "polywrap f",
        "valueG": "polywrap g",
        "valueH": "polywrap h",
        "valueI": "polywrap i",
        "valueJ": "polywrap j",
        "valueK": "polywrap k",
        "valueL": "polywrap l",
    }

    setDataWithManyArgs = client.invoke(
        uri=wrapper_uri(implementation),
        method="setDataWithManyArgs",
        args=args,
    )

    expected = "polywrap apolywrap bpolywrap cpolywrap dpolywrap epolywrap fpolywrap gpolywrap hpolywrap ipolywrap jpolywrap kpolywrap l"
    assert setDataWithManyArgs == expected

@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_set_data_with_many_structured_args(
    implementation: str, builder: ClientConfigBuilder, wrapper_uri: Callable[[str], Uri]
):
    client = PolywrapClient(builder.build())
    create_obj: Callable[[int], Dict[str, str]] = lambda i: {
        "propA": f"a-{i}",
        "propB": f"b-{i}",
        "propC": f"c-{i}",
        "propD": f"d-{i}",
        "propE": f"e-{i}",
        "propF": f"f-{i}",
        "propG": f"g-{i}",
        "propH": f"h-{i}",
        "propI": f"i-{i}",
        "propJ": f"j-{i}",
        "propK": f"k-{i}",
        "propL": f"l-{i}",
    }
    args = {
        "valueA": create_obj(1),
        "valueB": create_obj(2),
        "valueC": create_obj(3),
        "valueD": create_obj(4),
        "valueE": create_obj(5),
        "valueF": create_obj(6),
        "valueG": create_obj(7),
        "valueH": create_obj(8),
        "valueI": create_obj(9),
        "valueJ": create_obj(10),
        "valueK": create_obj(11),
        "valueL": create_obj(12),
    }

    setDataWithManyStructuredArgs = client.invoke(
        uri=wrapper_uri(implementation),
        method="setDataWithManyStructuredArgs",
        args=args,
    )

    assert setDataWithManyStructuredArgs == True
