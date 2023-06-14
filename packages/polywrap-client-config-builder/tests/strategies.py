from polywrap_core import Uri, UriResolver, WrapPackage, Wrapper
from hypothesis import strategies as st
from unittest.mock import Mock

from polywrap_client_config_builder import BuilderConfig

from .consts import C_LONG_MAX, C_LONG_MIN

# List of Mock resolvers
MockResolvers = [Mock(UriResolver, name=f"MockResolver{i}") for i in range(10)]

# List of Mock wrappers
MockWrappers = [Mock(Wrapper, name=f"MockWrapper{i}") for i in range(10)]

# List of Mock packages
MockPackages = [Mock(WrapPackage, name=f"MockPackage{i}") for i in range(10)]

# Scalars
scalar_st_list = [
    st.none(),
    st.booleans(),
    st.integers(min_value=C_LONG_MIN, max_value=C_LONG_MAX),
    st.floats(allow_nan=False),
    st.text(),
    st.binary(),
]

# Uri 
uri_safe_chars_strategy = st.text(
    alphabet=st.characters(whitelist_categories="L", whitelist_characters="-._~")
)
uri_strategy = st.builds(Uri, uri_safe_chars_strategy, uri_safe_chars_strategy)

# Env
env_strategy = st.dictionaries(st.text(), st.one_of(scalar_st_list), max_size=10)
envs_strategy = st.dictionaries(
    uri_strategy, env_strategy, max_size=10
)

# Interface Implementations
interfaces_strategy = st.dictionaries(uri_strategy, st.lists(uri_strategy, max_size=10), max_size=10)

# Non-empty Interface Implementations
non_empty_interfaces_strategy = st.dictionaries(uri_strategy, st.lists(uri_strategy, min_size=1, max_size=10), min_size=1, max_size=10)

# URI Redirects
redirects_strategy = st.dictionaries(uri_strategy, uri_strategy, max_size=10)

# Resolver 
resolver_strategy = st.sampled_from(MockResolvers)
resolvers_strategy = st.lists(resolver_strategy, max_size=10)

# Wrapper
wrapper_strategy = st.sampled_from(MockWrappers)
wrappers_strategy = st.dictionaries(uri_strategy, wrapper_strategy, max_size=10)

# Packages
package_strategy = st.sampled_from(MockPackages)
packages_strategy = st.dictionaries(uri_strategy, package_strategy, max_size=10)

# builder config
builder_config_strategy = st.builds(
    BuilderConfig,
    envs=envs_strategy,
    interfaces=interfaces_strategy,
    wrappers=wrappers_strategy,
    packages=packages_strategy,
    resolvers=resolvers_strategy,
    redirects=redirects_strategy,
)
