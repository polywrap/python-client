from polywrap_core import (
    Uri,
    UriResolutionContext,
    build_clean_uri_history
)
from polywrap_client import PolywrapClient


def test_recursive_resolve_uri(client: PolywrapClient) -> None:
    uri = Uri.from_str("test/1")

    resolution_context = UriResolutionContext()
    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.recursive_resolve import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/4"
