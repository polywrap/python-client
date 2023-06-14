import pytest
from polywrap_core import Uri, UriResolutionContext, ClientConfig
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import RedirectResolver

@pytest.fixture
def client() -> PolywrapClient:
    resolver = RedirectResolver(Uri.from_str("test/from"), Uri.from_str("test/to"))
    return PolywrapClient(ClientConfig(resolver=resolver))

@pytest.fixture
def resolution_context() -> UriResolutionContext:
    return UriResolutionContext()

