from typing import Any, Dict
from hypothesis import assume, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import packages_strategy, uri_strategy, package_strategy


@settings(max_examples=100)
@given(packages=packages_strategy, new_uri=uri_strategy, new_package=package_strategy)
def test_set_package(packages: Dict[Uri, Any], new_uri: Uri, new_package: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {**packages}

    existing_uris = set(builder.config.packages.keys())
    assume(new_uri not in existing_uris)

    builder.set_package(new_uri, new_package)

    assert len(builder.config.packages) == len(existing_uris) + 1
    assert builder.config.packages[new_uri] == new_package


@settings(max_examples=100)
@given(uri=uri_strategy, old_package=package_strategy, new_package=package_strategy)
def test_set_env_overwrite(uri: Uri, old_package: Any, new_package: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {uri: old_package}

    builder.set_package(uri, new_package)

    assert builder.config.packages == {uri: new_package}


@settings(max_examples=100)
@given(initial_packages=packages_strategy, new_packages=packages_strategy)
def test_set_packages(
    initial_packages: Dict[Uri, Any],
    new_packages: Dict[Uri, Any],
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.packages = {**initial_packages}

    builder.set_packages(new_packages)

    assert len(builder.config.envs) <= len(initial_packages) + len(new_packages)
