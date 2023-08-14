Polywrap Ethereum Provider
==========================
This package provides a Polywrap plugin for interacting with EVM networks.

The Ethereum Provider plugin implements the `ethereum-provider-interface`     @ `ens/wraps.eth:ethereum-provider@2.0.0 <https://app.ens.domains/name/wraps.eth/details>`__     (see `../../interface/polywrap.graphql` ).     It handles Ethereum wallet transaction signatures and sends JSON RPC requests     for the Ethereum wrapper.

Quickstart
----------

Imports
~~~~~~~

>>> from polywrap_core import Uri
>>> from polywrap_client import PolywrapClient
>>> from polywrap_ethereum_provider import ethereum_provider_plugin
>>> from polywrap_ethereum_provider.connection import Connection
>>> from polywrap_ethereum_provider.connections import Connections
>>> from polywrap_ethereum_provider.networks import KnownNetwork
>>> from polywrap_client_config_builder import (
...     PolywrapClientConfigBuilder
... )

Configure Client
~~~~~~~~~~~~~~~~

>>> ethreum_provider_interface_uri = Uri.from_str("ens/wraps.eth:ethereum-provider@2.0.0")
>>> ethereum_provider_plugin_uri = Uri.from_str("plugin/ethereum-provider")
>>> connections = Connections(
...     connections={
...         "sepolia": Connection.from_network(KnownNetwork.sepolia, None)
...     },
...     default_network="sepolia"
... )
>>> client_config = (
...     PolywrapClientConfigBuilder()
...     .set_package(
...         ethereum_provider_plugin_uri,
...         ethereum_provider_plugin(connections=connections)
...     )
...     .add_interface_implementations(
...         ethreum_provider_interface_uri,
...         [ethereum_provider_plugin_uri]
...     )
...     .set_redirect(ethreum_provider_interface_uri, ethereum_provider_plugin_uri)
...     .build()
... )
>>> client = PolywrapClient(client_config)

Invocation
~~~~~~~~~~

>>> result = client.invoke(
...     uri=ethreum_provider_interface_uri,
...     method="request",
...     args={"method": "eth_chainId"},
...     encode_result=False,
... )
>>> print(result)
"0xaa36a7"
