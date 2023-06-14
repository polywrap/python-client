from polywrap_core import Uri, UriResolutionContext, build_clean_uri_history
from polywrap_client import PolywrapClient


def test_can_redirect_uri(
    client: PolywrapClient, resolution_context: UriResolutionContext
) -> None:
    uri = Uri.from_str("test/from")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.can_redirect import EXPECTED

    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/to"
