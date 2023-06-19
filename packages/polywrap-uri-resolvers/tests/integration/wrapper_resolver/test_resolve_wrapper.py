from polywrap_core import Uri, UriResolutionContext, UriWrapper, build_clean_uri_history
from polywrap_client import PolywrapClient


def test_resolve_wrapper(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/wrapper")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.resolve_wrapper import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriWrapper), "Expected a UriWrapper result."
    assert result.uri.uri == "wrap://test/wrapper"
