from polywrap_client import PolywrapClient
from polywrap_core import (
    ClientConfig,
    Uri,
    UriPackage,
    UriResolutionContext,
)
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    RecursiveResolver,
    StaticResolver,
    UriResolverAggregator,
    UriResolverExtensionError,
)
import pytest

from .mocker import mock_subinvoke_plugin_resolver, mock_plugin_extension_resolver, MockPluginExtensionResolver, MockSubinvokePluginResolver


@pytest.fixture
def client() -> PolywrapClient:
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                StaticResolver(
                    {
                        MockSubinvokePluginResolver.URI: UriPackage(
                            uri=MockSubinvokePluginResolver.URI,
                            package=mock_subinvoke_plugin_resolver(),
                        ),
                        MockPluginExtensionResolver.URI: UriPackage(
                            uri=MockPluginExtensionResolver.URI,
                            package=mock_plugin_extension_resolver(),
                        ),
                    }
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
                    MockSubinvokePluginResolver.URI
                ]
            },
        )
    )



def test_shows_error_with_plugin_extension_subinvoke(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri.from_str("test/error")

    with pytest.raises(UriResolverExtensionError) as excinfo:
        client.try_resolve_uri(uri=source_uri, resolution_context=resolution_context)

    assert (
        excinfo.value.args[0]
        == f"Failed to resolve uri: {source_uri}, using extension resolver: ({MockSubinvokePluginResolver.URI})"
    )
