from polywrap_client import PolywrapClient
from polywrap_core import Uri, UriResolutionContext


def test_same_resolution_path_after_caching(recursive_client: PolywrapClient):
    uri = Uri.from_str("test/A")
    expected_path = [
        Uri.from_str("wrap://test/A"),
        Uri.from_str("wrap://test/B"),
        Uri.from_str("wrap://test/wrapper"),
    ]

    resolution_context = UriResolutionContext()
    recursive_client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    resolution_path = resolution_context.get_resolution_path()
    assert resolution_path == expected_path

    resolution_context = UriResolutionContext()
    recursive_client.try_resolve_uri(uri=uri, resolution_context=resolution_context)

    resolution_path = resolution_context.get_resolution_path()
    assert resolution_path == expected_path
