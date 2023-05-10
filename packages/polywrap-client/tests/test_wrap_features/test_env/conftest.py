from typing import Callable

import pytest
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri
from polywrap_test_cases import get_path_to_test_wrappers
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader

from polywrap_client import Env


@pytest.fixture
def external_wrapper_uri() -> Callable[[str], Uri]:
    def get_external_wrapper_uri(implementation: str) -> Uri:
        external_wrapper_path = f"{get_path_to_test_wrappers()}/env-type/00-external/implementations/{implementation}"
        return Uri.from_str(f"file/{external_wrapper_path}")

    return get_external_wrapper_uri


@pytest.fixture
def wrapper_uri() -> Callable[[str], Uri]:
    def get_wrapper_uri(implementation: str) -> Uri:
        wrapper_path = f"{get_path_to_test_wrappers()}/env-type/01-main/implementations/{implementation}"
        return Uri.from_str(f"file/{wrapper_path}")

    return get_wrapper_uri


@pytest.fixture
def wrapper_env() -> Env:
    return {
        "object": {
            "prop": "object string",
        },
        "str": "string",
        "optFilledStr": "optional string",
        "number": 10,
        "bool": True,
        "en": "FIRST",
        "array": [32, 23],
    }


@pytest.fixture
def expected_wrapper_env(wrapper_env: Env) -> Env:
    return {
        **wrapper_env,
        "optStr": None,
        "optNumber": None,
        "optBool": None,
        "optObject": None,
        "optEnum": None,
        "en": 0,
    }


@pytest.fixture
def external_wrapper_env() -> Env:
    return {
        "externalArray": [1, 2, 3],
        "externalString": "iamexternal",
    }


@pytest.fixture
def builder(
    wrapper_uri: Callable[[str], Uri],
    external_wrapper_uri: Callable[[str], Uri],
    wrapper_env: Env,
    external_wrapper_env: Env,
) -> Callable[[str], ClientConfigBuilder]:
    def get_builder(implementation: str) -> ClientConfigBuilder:
        return (
            PolywrapClientConfigBuilder()
            .add_env(
                wrapper_uri(implementation),
                wrapper_env,
            )
            .add_env(
                external_wrapper_uri(implementation),
                external_wrapper_env,
            )
            .set_redirect(
                Uri.from_str("ens/external-env.polywrap.eth"),
                external_wrapper_uri(implementation),
            )
            .add_resolver(FsUriResolver(SimpleFileReader()))
        )

    return get_builder
