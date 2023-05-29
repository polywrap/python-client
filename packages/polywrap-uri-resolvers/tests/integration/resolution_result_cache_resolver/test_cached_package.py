from polywrap_core import (
    Uri,
    UriResolutionContext,
    UriPackage,
    build_clean_uri_history,
)
from polywrap_client import PolywrapClient


def test_cached_package(client: PolywrapClient):
    uri = Uri.from_str("test/package")

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.package_without_cache import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriPackage), "Expected a UriPackage result."
    assert result.uri.uri == "wrap://test/package"

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.package_with_cache import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriPackage), "Expected a UriPackage result."
    assert result.uri.uri == "wrap://test/package"
