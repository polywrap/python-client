import pytest
from polywrap_core import (
    Uri,
    UriPackage,
    UriResolutionContext,
    ClientConfig,
    UriWrapper,
)
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import StaticResolver


@pytest.fixture
def client() -> PolywrapClient:
    resolver = StaticResolver(
        {
            Uri.from_str("test/from"): Uri.from_str("test/to"),
            Uri.from_str("test/package"): UriPackage(
                uri=Uri.from_str("test/package"), package=NotImplemented
            ),
            Uri.from_str("test/wrapper"): UriWrapper(
                uri=Uri.from_str("test/wrapper"), wrapper=NotImplemented
            ),
        }
    )
    return PolywrapClient(ClientConfig(resolver=resolver))


@pytest.fixture
def resolution_context() -> UriResolutionContext:
    return UriResolutionContext()
