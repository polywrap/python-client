from polywrap_core import Uri, UriResolutionContext, UriPackage, build_clean_uri_history
from polywrap_client import PolywrapClient



def test_resolve_package(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/package")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    from .histories.resolve_package import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, UriPackage), "Expected a UriPackage result."
    assert result.uri.uri == "wrap://test/package"


def test_not_resolve_package(client: PolywrapClient, resolution_context: UriResolutionContext) -> None:
    uri = Uri.from_str("test/not-a-match")

    result = client.try_resolve_uri(uri=uri, resolution_context=resolution_context)
    
    from .histories.not_resolve_package import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED

    assert isinstance(result, Uri), "Expected a Uri result."
    assert result.uri == "wrap://test/not-a-match"
