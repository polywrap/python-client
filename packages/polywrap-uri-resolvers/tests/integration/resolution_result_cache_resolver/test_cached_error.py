from polywrap_core import (
    Uri,
    UriResolutionContext,
)
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import UriResolutionError
import pytest


def test_cached_error(client: PolywrapClient):
    client._config.resolver.cache_errors = True  # type: ignore

    resolution_context = UriResolutionContext()
    with pytest.raises(UriResolutionError) as exc_info_1:
        client.try_resolve_uri(
            uri=Uri.from_str("test/error"), resolution_context=resolution_context
        )

    assert exc_info_1.value.__class__.__name__ == "UriResolutionError"
    assert exc_info_1.value.args[0] == "A test error"

    resolution_context = UriResolutionContext()
    with pytest.raises(UriResolutionError) as exc_info_2:
        client.try_resolve_uri(
            uri=Uri.from_str("test/error"), resolution_context=resolution_context
        )

    assert exc_info_2.value.__class__.__name__ == "UriResolutionError"
    assert exc_info_2.value.args[0] == "A test error"

    assert exc_info_1.value is exc_info_2.value
