from polywrap_core import (
    Uri,
    UriResolutionContext,
    UriWrapper,
    build_clean_uri_history,
)
from polywrap_client import PolywrapClient


def test_cached_wrapper(client: PolywrapClient):
    uri = Uri.from_str("test/wrapper")

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.wrapper_without_cache import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriWrapper), "Expected a UriWrapper result."
    assert result.uri.uri == "wrap://test/wrapper"

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.wrapper_with_cache import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriWrapper), "Expected a UriWrapper result."
    assert result.uri.uri == "wrap://test/wrapper"
