Polywrap Ethereum Wallet
========================
This package provides a Polywrap plugin for interacting with EVM networks.

The Ethereum wallet plugin implements the `ethereum-provider-interface`     @ `wrapscan.io/polywrap/ethereum-wallet@1.0`     (see `../../interface/polywrap.graphql` ).     It handles Ethereum wallet transaction signatures and sends JSON RPC requests     for the Ethereum wrapper.

Quickstart
----------

Imports
~~~~~~~

>>> from polywrap_core import Uri
>>> from polywrap_client import PolywrapClient
>>> from polywrap_ethereum_wallet import ethereum_wallet_plugin
>>> from polywrap_ethereum_wallet.connection import Connection
>>> from polywrap_ethereum_wallet.connections import Connections
>>> from polywrap_ethereum_wallet.networks import KnownNetwork
>>> from polywrap_client_config_builder import (
...     PolywrapClientConfigBuilder
... )

Configure Client
~~~~~~~~~~~~~~~~

>>> ethreum_provider_interface_uri = Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0")
>>> ethereum_wallet_plugin_uri = Uri.from_str("plugin/ethereum-provider")
>>> connections = Connections(
...     connections={
...         "sepolia": Connection.from_network(KnownNetwork.sepolia, None)
...     },
...     default_network="sepolia"
... )
>>> client_config = (
...     PolywrapClientConfigBuilder()
...     .set_package(
...         ethereum_wallet_plugin_uri,
...         ethereum_wallet_plugin(connections=connections)
...     )
...     .add_interface_implementations(
...         ethreum_provider_interface_uri,
...         [ethereum_wallet_plugin_uri]
...     )
...     .set_redirect(ethreum_provider_interface_uri, ethereum_wallet_plugin_uri)
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
