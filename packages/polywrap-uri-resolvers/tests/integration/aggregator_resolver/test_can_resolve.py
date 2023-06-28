from polywrap_core import Uri, UriResolutionContext, build_clean_uri_history
from polywrap_client import PolywrapClient


def test_can_resolve_first(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/1")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.can_resolve_first import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/2"


def test_can_resolve_last(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/3")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.can_resolve_last import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/4"
