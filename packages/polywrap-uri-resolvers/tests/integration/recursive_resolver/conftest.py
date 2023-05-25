import pytest
from polywrap_core import (
    ClientConfig,
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
)
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import RecursiveResolver


class SimpleRedirectResolver:
    def try_resolve_uri(
        self, uri: Uri, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> UriPackageOrWrapper:
        result: UriPackageOrWrapper

        if uri.uri == "wrap://test/1":
            result = Uri.from_str("test/2")
        elif uri.uri == "wrap://test/2":
            result = Uri.from_str("test/3")
        elif uri.uri == "wrap://test/3":
            result = Uri.from_str("test/4")
        else:
            result = uri

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri, result=result, description="SimpleRedirectResolver"
            )
        )

        return result


@pytest.fixture
def simple_redirect_resolver() -> SimpleRedirectResolver:
    return SimpleRedirectResolver()


@pytest.fixture
def client(simple_redirect_resolver: SimpleRedirectResolver) -> PolywrapClient:
    resolver = RecursiveResolver(simple_redirect_resolver)
    return PolywrapClient(ClientConfig(resolver=resolver))
