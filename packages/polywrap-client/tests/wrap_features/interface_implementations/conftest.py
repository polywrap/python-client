from typing import Callable

import pytest
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri
from polywrap_test_cases import get_path_to_test_wrappers
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


@pytest.fixture
def interface_uri() -> Uri:
    return Uri.from_str("wrap://ens/interface.eth")


@pytest.fixture
def implementation_uri() -> Callable[[str], Uri]:
    def get_implementation_uri(implementation: str) -> Uri:
        implementation_path = f"{get_path_to_test_wrappers()}/interface-invoke/01-implementation/implementations/{implementation}"
        return Uri.from_str(f"file/{implementation_path}")

    return get_implementation_uri


@pytest.fixture
def wrapper_uri() -> Callable[[str], Uri]:
    def get_wrapper_uri(implementation: str) -> Uri:
        wrapper_path = f"{get_path_to_test_wrappers()}/interface-invoke/02-wrapper/implementations/{implementation}"
        return Uri.from_str(f"file/{wrapper_path}")

    return get_wrapper_uri


@pytest.fixture
def builder(
    interface_uri: Uri,
    implementation_uri: Callable[[str], Uri],
) -> Callable[[str], ClientConfigBuilder]:
    def get_builder(implementation: str) -> ClientConfigBuilder:
        return (
            PolywrapClientConfigBuilder()
            .add_interface_implementations(
                interface_uri=interface_uri,
                implementations_uris=[implementation_uri(implementation)]
            )
            .add_resolver(FsUriResolver(SimpleFileReader()))
        )

    return get_builder
