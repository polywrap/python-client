from typing import Dict, cast
from unittest.mock import patch
from polywrap_uri_resolvers import (
    PackageResolver,
    RecursiveResolver,
    StaticResolver,
    UriResolverAggregator,
    ResolutionResultCacheResolver,
    ExtendableUriResolver,
    InMemoryResolutionResultCache,
)
from polywrap_client_config_builder import (
    BuildOptions,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri, UriPackage, UriWrapper, WrapPackage, Wrapper
import pytest


@pytest.fixture
def builder() -> PolywrapClientConfigBuilder:
    """Return a PolywrapClientConfigBuilder with a default config."""
    return PolywrapClientConfigBuilder()


def test_build_resolver_order(builder: PolywrapClientConfigBuilder):
    """Test the order of resolvers in UriResolverAggregator."""
    redirects: Dict[Uri, Uri] = {Uri.from_str("test/1"): Uri.from_str("test/2")}
    builder.config.redirects = redirects

    config = builder.build()

    isinstance(config.resolver, RecursiveResolver)
    recursive_resolver = cast(RecursiveResolver, config.resolver)

    isinstance(recursive_resolver.resolver, ResolutionResultCacheResolver)
    cache_resolver = cast(ResolutionResultCacheResolver, recursive_resolver.resolver)

    isinstance(cache_resolver.resolver_to_cache, UriResolverAggregator)
    aggregator_resolver = cast(UriResolverAggregator, cache_resolver.resolver_to_cache)

    aggregated_resolvers = aggregator_resolver._resolvers  # type: ignore
    assert isinstance(aggregated_resolvers[0], StaticResolver)
    assert isinstance(aggregated_resolvers[1], ExtendableUriResolver)


def test_no_build_options(builder: PolywrapClientConfigBuilder):
    """Test the absence of resolver in BuildOptions."""
    config = builder.build()
    assert isinstance(config.resolver, RecursiveResolver)


def test_build_options_resolver(builder: PolywrapClientConfigBuilder):
    """Test the presence of resolver in BuildOptions overrides the default one."""
    redirects: Dict[Uri, Uri] = {Uri.from_str("test/1"): Uri.from_str("test/2")}
    builder.config.redirects = redirects

    config = builder.build(
        BuildOptions(
            resolver=PackageResolver(
                uri=Uri.from_str("test/package"), package=NotImplemented
            )
        )
    )

    assert isinstance(config.resolver, PackageResolver)


def test_build_options_cache(builder: PolywrapClientConfigBuilder):
    """Test the presence of cache in BuildOptions overrides the default one."""
    custom_cache = InMemoryResolutionResultCache()
    config = builder.build(BuildOptions(resolution_result_cache=custom_cache))
    assert isinstance(config.resolver, RecursiveResolver)
    assert isinstance(config.resolver.resolver, ResolutionResultCacheResolver)

    assert config.resolver.resolver.cache is custom_cache


def test_build_static_resolver_like(builder: PolywrapClientConfigBuilder):
    """Test the composition of StaticResolverLike."""
    redirects: Dict[Uri, Uri] = {Uri.from_str("test/from"): Uri.from_str("test/to")}
    builder.config.redirects = redirects

    with patch("polywrap_core.types.wrapper.Wrapper") as MockWrapper, patch(
        "polywrap_core.types.wrap_package.WrapPackage"
    ) as MockPackage:

        wrappers: Dict[Uri, Wrapper] = {Uri.from_str("test/wrapper"): MockWrapper}
        builder.config.wrappers = wrappers

        packages: Dict[Uri, WrapPackage] = {Uri.from_str("test/package"): MockPackage}
        builder.config.packages = packages

        static_resolver_like = builder._build_static_resolver_like()  # type: ignore

        assert static_resolver_like[Uri.from_str("test/from")] == Uri.from_str(
            "test/to"
        )
        assert static_resolver_like[Uri.from_str("test/wrapper")] == UriWrapper(
            uri=Uri.from_str("test/wrapper"), wrapper=MockWrapper
        )
        assert static_resolver_like[Uri.from_str("test/package")] == UriPackage(
            uri=Uri.from_str("test/package"), package=MockPackage
        )


def test_build_client_config_attributes(builder: PolywrapClientConfigBuilder):
    """Test the attributes of ClientConfig."""
    envs = {Uri("test", "env1"): "test", Uri("test", "env2"): "test"}
    builder.config.envs = envs

    interfaces = {
        Uri("test", "interface1"): [Uri("test", "impl1"), Uri("test", "impl2")],
        Uri("test", "interface2"): [Uri("test", "impl3")],
    }
    builder.config.interfaces = interfaces

    config = builder.build()

    assert config.envs is envs
    assert config.interfaces is interfaces
