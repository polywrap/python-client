from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_msgpack import GenericMap
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_return_map_when_map(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("map-type", implementation)
    map_value = GenericMap({"Hello": 1, "World": 2})

    response = client.invoke(
        uri=uri,
        method="returnMap",
        args={
            "map": map_value,
        },
    )

    assert response == map_value


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_return_map_when_dict(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("map-type", implementation)
    map_value = {"Hello": 1, "World": 2}

    response = client.invoke(
        uri=uri,
        method="returnMap",
        args={
            "map": map_value,
        },
    )

    assert response == GenericMap(map_value)


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_get_key(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("map-type", implementation)
    map_value = {"Hello": 1, "World": 2}
    nested_map_value = {"Nested": map_value}

    response = client.invoke(
        uri=uri,
        method="getKey",
        args={
            "foo": {
                "map": map_value,
                "nestedMap": nested_map_value,
            },
            "key": "Hello",
        },
    )

    assert response == 1


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_return_custom_map(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("map-type", implementation)
    map_value = GenericMap({"Hello": 1, "World": 2})
    nested_map_value = GenericMap({"Nested": map_value})
    foo = {
        "map": map_value,
        "nestedMap": nested_map_value,
    }

    response = client.invoke(
        uri=uri,
        method="returnCustomMap",
        args={
            "foo": foo,
        },
    )

    assert response == foo


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_return_nested_map(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("map-type", implementation)
    map_value = GenericMap({"Hello": 1, "World": 2})
    nested_map_value = GenericMap({"Nested": map_value})

    response = client.invoke(
        uri=uri,
        method="returnNestedMap",
        args={
            "foo": nested_map_value,
        },
    )

    assert response == nested_map_value
