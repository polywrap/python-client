import pytest
from polywrap_core import (
    ClientConfig,
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriWrapper,
    UriPackage,
    UriResolver,
)
from polywrap_client import PolywrapClient
from polywrap_uri_resolvers import (
    RecursiveResolver,
    ResolutionResultCacheResolver,
    UriResolutionError,
    InMemoryResolutionResultCache,
)


class TestResolver(UriResolver):
    def try_resolve_uri(
        self, uri: Uri, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> UriPackageOrWrapper:
        result: UriPackageOrWrapper

        if uri.uri == "wrap://test/package":
            result = UriPackage(uri=uri, package=NotImplemented)
        elif uri.uri == "wrap://test/wrapper":
            result = UriWrapper(uri=uri, wrapper=NotImplemented)
        elif uri.uri == "wrap://test/from":
            result = Uri.from_str("test/to")
        elif uri.uri == "wrap://test/A":
            result = Uri.from_str("test/B")
        elif uri.uri == "wrap://test/B":
            result = Uri.from_str("test/wrapper")
        elif uri.uri == "wrap://test/error":
            raise UriResolutionError("A test error")
        else:
            raise UriResolutionError(f"Unexpected URI: {uri.uri}")

        resolution_context.track_step(
            UriResolutionStep(source_uri=uri, result=result, description="TestResolver")
        )

        return result


@pytest.fixture
def client():
    resolver = ResolutionResultCacheResolver(
        TestResolver(), cache=InMemoryResolutionResultCache()
    )
    return PolywrapClient(ClientConfig(resolver=resolver))


@pytest.fixture
def recursive_client():
    resolver = RecursiveResolver(
        ResolutionResultCacheResolver(
            TestResolver(), cache=InMemoryResolutionResultCache()
        )
    )
    return PolywrapClient(ClientConfig(resolver=resolver))
