from typing import Any, Dict
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import packages_strategy


@settings(max_examples=100)
@given(packages=packages_strategy)
def test_get_package_exists(
    packages: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = packages

    for uri in packages:
        assert builder.get_package(uri) == packages[uri]
    assert builder.get_package(Uri.from_str("test/not-exists")) is None


def test_get_package_not_exists():
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_package(Uri.from_str("test/not-exists")) is None


@settings(max_examples=100)
@given(packages=packages_strategy)
def test_get_packages(
    packages: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_packages() == {}

    builder.config.packages = packages
    assert builder.get_packages() == packages
