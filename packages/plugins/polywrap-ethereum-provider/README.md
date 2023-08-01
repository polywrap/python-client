# polywrap-ethereum-plugin
The Ethereum Provider plugin implements the `ethereum-provider-interface` @ [ens/wraps.eth:ethereum-provider@2.0.0](https://app.ens.domains/name/wraps.eth/details) (see [../../interface/polywrap.graphql](../../interface/polywrap.graphql)). It handles Ethereum wallet transaction signatures and sends JSON RPC requests for the Ethereum wrapper.

## Usage
### 1. Configure Client
When creating your Polywrap Python client, add the ethereum wallet plugin:
```python
from polywrap_client import PolywrapClient
from polywrap_ethereum_provider import ethereum_provider_plugin

ethereum_provider_plugin_uri = Uri.from_str("plugin/ethereum-provider")
connections = Connections(
    connections={
        "mocknet": Connection(provider, None),
        "sepolia": Connection.from_network(KnownNetwork.sepolia, None)
    },
    default_network="sepolia",
    signer=account.key if with_signer else None,  # type: ignore
)

ethreum_provider_interface_uri = Uri.from_str("ens/wraps.eth:ethereum-provider@2.0.0")

client_config = (
    PolywrapClientConfigBuilder()
    .set_package(ethereum_provider_plugin_uri, ethereum_provider_plugin(connections=connections))
    .add_interface_implementations(ethreum_provider_interface_uri, [ethereum_provider_plugin_uri])
    .set_redirect(ethreum_provider_interface_uri, ethereum_provider_plugin_uri)
    .build()
)
client = PolywrapClient(client_config)
```

### 2. Invoke The Ethereum Wrapper
Invocations to the Ethereum wrapper may trigger sub-invocations to the Ethereum Provider plugin:
```python
client.invoke(
  uri=ethreum_provider_interface_uri,
  method="getSignerAddress",
);
```
