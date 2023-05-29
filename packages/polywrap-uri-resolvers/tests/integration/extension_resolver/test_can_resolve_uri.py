from polywrap_client import PolywrapClient
from polywrap_core import Uri, UriResolutionContext, build_clean_uri_history


def test_can_resolve_first(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri.from_str("test/from")
    redirected_uri = Uri.from_str("test/to")

    result = client.try_resolve_uri(
        uri=source_uri, resolution_context=resolution_context
    )

    from .histories.can_resolve_uri import EXPECTED

    print(build_clean_uri_history(resolution_context.get_history()) )

    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result == redirected_uri
