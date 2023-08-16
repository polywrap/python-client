# Ens Wrap Example

In this example, we demonstrate how to use the
`PolywrapClient` to communicate with the Ethereum network.
The code focuses on interacting with the Ethereum Name Service (ENS) to
resolve addresses and fetch content hashes.

## Setup and Dependencies

We first import the necessary libraries and modules:

<!-- name: test_ens -->
```python
from polywrap import (
    Uri,
    PolywrapClient,
    PolywrapClientConfigBuilder,
    ethereum_provider_plugin,
    Connections,
    Connection,
    sys_bundle
)
```

## Initialization

We define our domain and ENS URI:

<!-- name: test_ens -->
```python
domain = "vitalik.eth"
ens_uri = Uri.from_str("wrapscan.io/polywrap/ens@1.0.0")
```

## Configuring the Polywrap Client

To interact with the Ethereum network, we set up a configuration for the
`PolywrapClient`. This involves:

1.  Instantiating a `PolywrapClientConfigBuilder`.
2.  Adding the required bundles.
3.  Setting up the Ethereum network connection.
4.  Configuring the Ethereum wallet plugin.

<!-- name: test_ens -->
```python
builder = PolywrapClientConfigBuilder()
builder.add_bundle(sys_bundle)

mainnet_connection = Connection.from_node("https://mainnet.infura.io/v3/f1f688077be642c190ac9b28769daecf")
connections = Connections({
    "mainnet": mainnet_connection,
}, default_network="mainnet")

wallet_plugin = ethereum_provider_plugin(connections)
builder.set_package(Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0"), wallet_plugin)
config = builder.build()
client = PolywrapClient(config)
```

## Fetching Resolver Address

Next, we make an invocation to get the resolver address for our
specified ENS domain:

<!-- name: test_ens -->
```python
resolver_address = client.invoke(
    uri=ens_uri,
    method="getResolver",
    args={
        "registryAddress": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
        "domain": domain
    }
)
print(f"Resolver address: {resolver_address}")
assert resolver_address is not None
assert len(resolver_address) == 42
```

## Fetching Content Hash

Finally, we use the previously retrieved resolver address to fetch the
content hash of our ENS domain:

<!-- name: test_ens -->
```python
content_hash = client.invoke(
    uri=ens_uri,
    method="getContentHash",
    args={
        "resolverAddress": resolver_address,
        "domain": domain
    }
)
print(f"Content hash of {domain}: {content_hash}")
assert content_hash is not None
assert len(content_hash) == 78
```

## Conclusion

This example demonstrates how to use the `PolywrapClient` to interact with the ENS.
For more information on the `PolywrapClient`, please refer to the 
[Polywrap Python Client documentation](https://polywrap-client.rtfd.io).
