from polywrap_core import Uri, UriResolutionContext, build_clean_uri_history
from polywrap_client import PolywrapClient


def test_no_match(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/no-match")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.not_resolve import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/no-match"

