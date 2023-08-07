"""This package contains modules related to ClientConfigBuilder - \
  A utility class for building the PolywrapClient config.

PolywrapClientConfigBuilder Supports building configs using method chaining or imperatively.

Quickstart
----------

Import
~~~~~~

Import necessary modules

>>> from typing import cast
>>> from polywrap_client_config_builder import (
...     PolywrapClientConfigBuilder,
...     BuilderConfig,
...     BuildOptions,
... )
>>> from polywrap_core import WrapPackage, Uri, ClientConfig
>>> from polywrap_uri_resolvers import (
...     RedirectResolver,
...     InMemoryResolutionResultCache,
...     RecursiveResolver,
... )
>>> from polywrap_sys_config_bundle import sys_bundle
>>> from polywrap_web3_config_bundle import web3_bundle

Initialize
~~~~~~~~~~

Initialize a `PolywrapClientConfigBuilder` using the constructor

>>> # start with a blank slate (typical usage)
>>> builder = PolywrapClientConfigBuilder()

Configure
~~~~~~~~~

**Add client configuration with add, or flexibly mix and match \
  builder configuration methods to add and remove configuration items.**

Add multiple items to the configuration using the catch-all `add` method

>>> builder = builder.add(
...     BuilderConfig(
...         envs={},
...         interfaces={},
...         redirects={},
...         wrappers={},
...         packages={},
...         resolvers=[]
...     )
... )

Add or remove items by chaining method calls

>>> builder = (
...     builder
...     .set_package(Uri.from_str("wrap://plugin/package"), cast(WrapPackage, NotImplemented))
...     .remove_package(Uri.from_str("wrap://plugin/package"))
...     .set_packages(
...         {
...             Uri.from_str("wrap://plugin/http"): cast(WrapPackage, NotImplemented),
...             Uri.from_str("wrap://plugin/filesystem"): cast(WrapPackage, NotImplemented),
...         }
...     )
... )
>>> Uri.from_str("wrap://plugin/http") in builder.config.packages
True
>>> Uri.from_str("wrap://plugin/filesystem") in builder.config.packages
True
>>> Uri.from_str("wrap://plugin/package") in builder.config.packages
False


Configure using sys config bundle to fetch wraps from file-system, ipfs, wrapscan, or http server

>>> from polywrap_sys_config_bundle import sys_bundle
>>> builder = builder.add_bundle(sys_bundle)

Configure using web3 config bundle to fetch wraps from ens and any system URI

>>> from polywrap_web3_config_bundle import web3_bundle
>>> builder = builder.add_bundle(web3_bundle)

Build
~~~~~

**Finally, build a ClientConfig to pass to the PolywrapClient constructor.**

Accepted by the PolywrapClient

>>> config = builder.build()
>>> assert isinstance(config, ClientConfig)
>>> assert isinstance(config.resolver, RecursiveResolver)

Build with a custom cache

>>> config = builder.build(
...     BuildOptions(
...         resolution_result_cache=InMemoryResolutionResultCache()
...     )
... )
>>> assert isinstance(config, ClientConfig)
>>> assert isinstance(config.resolver, RecursiveResolver)

Or build with a custom resolver

>>> config = builder.build(
...     BuildOptions(
...         resolver=RedirectResolver(
...             from_uri=Uri.from_str("wrap://test/from"),
...             to_uri=Uri.from_str("wrap://test/to")
...         )
...     )
... )
>>> assert isinstance(config, ClientConfig)
>>> assert isinstance(config.resolver, RedirectResolver)
"""

from .polywrap_client_config_builder import *
from .types import *
