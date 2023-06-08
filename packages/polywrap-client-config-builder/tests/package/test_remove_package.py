from typing import Any, Dict
from random import randint
from hypothesis import assume, event, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import packages_strategy


@settings(max_examples=100)
@given(packages=packages_strategy)
def test_remove_package(packages: Dict[Uri, Any]):
    assume(packages)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {**packages}

    uris = list(packages.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_uri = uris[uri_index]
    event(f"Uri to remove: {remove_uri}")

    builder.remove_package(remove_uri)
    assert len(builder.config.packages) == len(packages) - 1
    assert remove_uri not in builder.config.packages


@settings(max_examples=100)
@given(packages=packages_strategy)
def test_remove_non_existent_package(packages: Dict[Uri, Any]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {**packages}

    builder.remove_package(Uri("test", "non-existent"))
    assert builder.config.packages == packages


@settings(max_examples=100)
@given(packages=packages_strategy)
def test_remove_packages(packages: Dict[Uri, Any]):
    assume(packages)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {**packages}

    uris = list(packages.keys())
    uri_indices = [
        randint(0, len(uris) - 1) for _ in range(randint(0, len(uris) - 1))
    ]
    remove_uris = list({uris[uri_index] for uri_index in uri_indices})
    event(f"Uris to remove: {remove_uris}")

    builder.remove_packages(remove_uris)
    assert len(builder.config.packages) == len(packages) - len(remove_uris)
    assert set(remove_uris) & set(builder.config.packages.keys()) == set()


