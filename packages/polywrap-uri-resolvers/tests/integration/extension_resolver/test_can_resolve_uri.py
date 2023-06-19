from polywrap_client import PolywrapClient
from polywrap_core import (
    ClientConfig,
    Uri,
    UriResolutionContext,
    build_clean_uri_history,
)
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    RecursiveResolver,
    UriResolverAggregator,
    PackageResolver,
)
import pytest

from .mocker import mock_plugin_extension_resolver, MockPluginExtensionResolver


@pytest.fixture
def client() -> PolywrapClient:
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                PackageResolver(
                    MockPluginExtensionResolver.URI,
                    mock_plugin_extension_resolver(),
                ),
                ExtendableUriResolver(),
            ]
        )
    )
    return PolywrapClient(
        ClientConfig(
            resolver=resolver,
            interfaces={
                ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS[0]: [
                    MockPluginExtensionResolver.URI
                ]
            },
        )
    )


def test_can_resolve_uri_with_plugin_extension(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri.from_str("test/from")
    redirected_uri = Uri.from_str("test/to")

    result = client.try_resolve_uri(
        uri=source_uri, resolution_context=resolution_context
    )

    from .histories.can_resolve_uri import EXPECTED
    assert isinstance(result, Uri), "Expected a Uri result."
    assert result == redirected_uri
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED
