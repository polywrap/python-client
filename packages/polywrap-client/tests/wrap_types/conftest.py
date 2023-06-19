from typing import Callable

import pytest
from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri
from polywrap_test_cases import get_path_to_test_wrappers
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


@pytest.fixture
def builder() -> ClientConfigBuilder:
    return PolywrapClientConfigBuilder().add_resolver(FsUriResolver(SimpleFileReader()))


@pytest.fixture
def wrapper_uri() -> Callable[[str, str], Uri]:
    def get_wrapper_uri(wrapper_name: str, implementation: str) -> Uri:
        wrapper_path = f"{get_path_to_test_wrappers()}/{wrapper_name}/implementations/{implementation}"
        return Uri.from_str(f"file/{wrapper_path}")

    return get_wrapper_uri
