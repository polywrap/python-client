import pytest
from polywrap_core import Uri, UriResolutionContext, ClientConfig
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import WrapperResolver

@pytest.fixture
def client() -> PolywrapClient:
    resolver = WrapperResolver(Uri.from_str("test/wrapper"), NotImplemented)
    return PolywrapClient(ClientConfig(resolver=resolver))

@pytest.fixture
def resolution_context() -> UriResolutionContext:
    return UriResolutionContext()

