from typing import Any, Dict
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import redirects_strategy


@settings(max_examples=100)
@given(redirects=redirects_strategy)
def test_get_redirect_exists(
    redirects: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = redirects

    for uri in redirects:
        assert builder.get_redirect(uri) == redirects[uri]
    assert builder.get_redirect(Uri.from_str("test/not-exists")) is None


def test_get_redirect_not_exists():
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_redirect(Uri.from_str("test/not-exists")) is None


@settings(max_examples=100)
@given(redirects=redirects_strategy)
def test_get_redirects(
    redirects: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_redirects() == {}

    builder.config.redirects = redirects
    assert builder.get_redirects() == redirects
