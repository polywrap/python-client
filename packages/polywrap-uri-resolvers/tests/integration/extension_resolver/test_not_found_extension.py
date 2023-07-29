from polywrap_client import PolywrapClient
from polywrap_core import (
    ClientConfig,
    Uri,
    UriResolutionContext,
)
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    RecursiveResolver,
    UriResolverAggregator,
    UriResolverExtensionError,
)
import pytest


@pytest.fixture
def client() -> PolywrapClient:
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                ExtendableUriResolver(),
            ]
        )
    )
    return PolywrapClient(
        ClientConfig(
            resolver=resolver,
            interfaces={
                ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS[0]: [
                    Uri.from_str("test/undefined-resolver")
                ]
            },
        )
    )


def test_can_resolve_uri_with_plugin_extension(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri.from_str("test/not-a-match")

    with pytest.raises(UriResolverExtensionError):
        client.try_resolve_uri(
            uri=source_uri, resolution_context=resolution_context
        )
