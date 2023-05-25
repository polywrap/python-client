import pytest
from polywrap_core import Uri, UriResolutionContext, ClientConfig
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import PackageResolver

@pytest.fixture
def client() -> PolywrapClient:
    resolver = PackageResolver(Uri.from_str("test/package"), NotImplemented)
    return PolywrapClient(ClientConfig(resolver=resolver))

@pytest.fixture
def resolution_context() -> UriResolutionContext:
    return UriResolutionContext()

