import os
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
from polywrap_test_cases import get_path_to_test_wrappers
import pytest

from .mocker import mock_fs_wasm_package_resolver


@pytest.fixture
def client() -> PolywrapClient:
    uri_package = mock_fs_wasm_package_resolver()
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                PackageResolver(
                    uri_package.uri,
                    uri_package.package,
                ),
                ExtendableUriResolver(),
            ]
        )
    )
    return PolywrapClient(
        ClientConfig(
            resolver=resolver,
            interfaces={
                ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS[0]: [uri_package.uri]
            },
        )
    )


def test_can_use_wasm_fs_resolver(client: PolywrapClient) -> None:
    resolution_context = UriResolutionContext()
    source_uri = Uri(
        "fs",
        os.path.join(get_path_to_test_wrappers(), "asyncify", "implementations", "as"),
    )

    result = client.try_resolve_uri(
        uri=source_uri, resolution_context=resolution_context
    )

    from .histories.can_use_wasm_fs_resolver import EXPECTED
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED
    
    # Note: real wasm fs resolver should returns a UriPackage, not a Uri.
    assert isinstance(result, Uri), "Expected a Uri result."