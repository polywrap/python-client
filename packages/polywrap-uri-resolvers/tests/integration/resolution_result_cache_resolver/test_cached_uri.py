from polywrap_core import (
    Uri,
    UriResolutionContext,
    build_clean_uri_history,
)
from polywrap_client import PolywrapClient


def test_cached_uri(client: PolywrapClient):
    uri = Uri.from_str("test/from")

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.uri_without_cache import EXPECTED

    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/to"

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.uri_with_cache import EXPECTED

    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/to"
