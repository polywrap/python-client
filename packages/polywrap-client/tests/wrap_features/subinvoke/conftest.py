from typing import Callable

import pytest
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri
from polywrap_test_cases import get_path_to_test_wrappers
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


@pytest.fixture
def subinvoke_wrapper_uri() -> Callable[[str], Uri]:
    def get_subinvoke_wrapper_uri(implementation: str) -> Uri:
        subinvoke_wrapper_path = f"{get_path_to_test_wrappers()}/subinvoke/00-subinvoke/implementations/{implementation}"
        return Uri.from_str(f"file/{subinvoke_wrapper_path}")

    return get_subinvoke_wrapper_uri


@pytest.fixture
def wrapper_uri() -> Callable[[str], Uri]:
    def get_wrapper_uri(implementation: str) -> Uri:
        wrapper_path = f"{get_path_to_test_wrappers()}/subinvoke/01-invoke/implementations/{implementation}"
        return Uri.from_str(f"file/{wrapper_path}")

    return get_wrapper_uri


@pytest.fixture
def builder(
    subinvoke_wrapper_uri: Callable[[str], Uri],
) -> Callable[[str], ClientConfigBuilder]:
    def get_builder(implementation: str) -> ClientConfigBuilder:
        return (
            PolywrapClientConfigBuilder()
            .set_redirect(
                Uri.from_str("ens/imported-subinvoke.eth"),
                subinvoke_wrapper_uri(implementation),
            )
            .add_resolver(FsUriResolver(SimpleFileReader()))
        )

    return get_builder
