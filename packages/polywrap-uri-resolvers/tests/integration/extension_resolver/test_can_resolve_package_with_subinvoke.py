from polywrap_client import PolywrapClient
from polywrap_core import (
    ClientConfig,
    Uri,
    UriPackage,
    UriResolutionContext,
    build_clean_uri_history,
)
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    RecursiveResolver,
    StaticResolver,
    UriResolverAggregator,
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
                        MockPluginExtensionResolver.URI: UriPackage(
                            uri=MockPluginExtensionResolver.URI,
                            package=mock_plugin_extension_resolver(),
                        ),
                        MockSubinvokePluginResolver.URI: UriPackage(
                            uri=MockSubinvokePluginResolver.URI,
                            package=mock_subinvoke_plugin_resolver(),
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


def test_can_resolve_package_with_plugin_extension(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri.from_str("test/package")

    result = client.try_resolve_uri(
        uri=source_uri, resolution_context=resolution_context
    )

    from .histories.can_resolve_package_with_subinvoke import EXPECTED
    print(build_clean_uri_history(resolution_context.get_history()))
    assert isinstance(result, UriPackage), "Expected a UriPackage result."
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED
