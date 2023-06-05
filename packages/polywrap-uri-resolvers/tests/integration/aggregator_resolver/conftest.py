import pytest
from polywrap_core import Uri, UriResolutionContext, ClientConfig
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import UriResolverAggregator, RedirectResolver

@pytest.fixture
def client() -> PolywrapClient:
    resolver = UriResolverAggregator([
        RedirectResolver(Uri.from_str("test/1"), Uri.from_str("test/2")),
        RedirectResolver(Uri.from_str("test/2"), Uri.from_str("test/3")),
        RedirectResolver(Uri.from_str("test/3"), Uri.from_str("test/4")),
    ], "TestAggregator")
    return PolywrapClient(ClientConfig(resolver=resolver))

@pytest.fixture
def resolution_context() -> UriResolutionContext:
    return UriResolutionContext()

