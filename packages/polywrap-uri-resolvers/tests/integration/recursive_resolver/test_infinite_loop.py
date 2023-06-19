import pytest
from polywrap_core import (
    ClientConfig,
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    build_clean_uri_history,
)
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import RecursiveResolver, InfiniteLoopError


class InfiniteRedirectResolver:
    def try_resolve_uri(
        self, uri: Uri, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> UriPackageOrWrapper:
        result: UriPackageOrWrapper

        if uri.uri == "wrap://test/1":
            result = Uri.from_str("test/2")
        elif uri.uri == "wrap://test/2":
            result = Uri.from_str("test/3")
        elif uri.uri == "wrap://test/3":
            result = Uri.from_str("test/1")
        else:
            result = uri

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri, result=result, description="InfiniteRedirectResolver"
            )
        )

        return result


@pytest.fixture
def infinite_redirect_resolver() -> InfiniteRedirectResolver:
    return InfiniteRedirectResolver()


@pytest.fixture
def client(infinite_redirect_resolver: InfiniteRedirectResolver) -> PolywrapClient:
    resolver = RecursiveResolver(infinite_redirect_resolver)
    return PolywrapClient(ClientConfig(resolver=resolver))


def test_infinite_loop(client: PolywrapClient):
    uri = Uri.from_str("test/1")
    resolution_context = UriResolutionContext()

    with pytest.raises(InfiniteLoopError) as excinfo:
        client.try_resolve_uri(uri=uri, resolution_context=resolution_context)
    from .histories.infinite_loop import EXPECTED
    assert excinfo.value.uri == uri
    assert build_clean_uri_history(resolution_context.get_history()) == EXPECTED
