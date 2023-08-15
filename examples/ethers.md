# Ethers Wrap Example

This documentation demonstrates the use of `PolywrapClient`
to interact with the Ethereum network. The objective is to retrieve
balance in Wei and Eth, and to sign typed data.

## Setup and Dependencies

First, we import the required libraries and modules:

<!-- name: test_ethers -->
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
import json
```

## Wrap URIs Initialization

Here, we define the URIs for ethers core and utility wraps:

<!-- name: test_ethers -->
```python
ethers_core_uri = Uri.from_str("wrapscan.io/polywrap/ethers@1.0.0")
ethers_util_uri = Uri.from_str("wrapscan.io/polywrap/ethers-utils@1.0.0")
```

## Configuring the Polywrap Client

For interacting with the Ethereum network, we configure the
`PolywrapClient`:

<!-- name: test_ethers -->
```python
builder = PolywrapClientConfigBuilder()
builder.add_bundle(sys_bundle)

mainnet_connection = Connection.from_node(
    "https://mainnet.infura.io/v3/f1f688077be642c190ac9b28769daecf",
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"  # Caution: Private key
)
connections = Connections({
    "mainnet": mainnet_connection,
}, default_network="mainnet")

wallet_plugin = ethereum_provider_plugin(connections)
builder.set_package(Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0"), wallet_plugin)
config = builder.build()
client = PolywrapClient(config)
```

## Fetching Balance

Retrieve the balance in both Wei and Eth:

<!-- name: test_ethers -->
```python
balance = client.invoke(
    uri=ethers_core_uri,
    method="getBalance",
    args={"address": "0x00000000219ab540356cbb839cbe05303d7705fa"}
)
print(f"Balance in Wei: {balance}")
assert int(balance) > 0

balance_in_eth = client.invoke(
    uri=ethers_util_uri,
    method="toEth",
    args={"wei": balance}
)
print(f"Balance in Eth: {balance_in_eth}")
```

## Signing Typed Data

To sign typed data, we define domain data, message, and types:

<!-- name: test_ethers -->
```python
domain_data = {
    "name": "Ether Mail",
    "version": "1",
    "chainId": 1,
    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"
}
message = {
    "from": {"name": "Cow", "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"},
    "to": {"name": "Bob", "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"},
    "contents": "Hello, Bob!"
}
types = {
    "EIP712Domain": [
        {"type": "string", "name": "name"},
        {"type": "string", "name": "version"},
        {"type": "uint256", "name": "chainId"},
        {"type": "address", "name": "verifyingContract"}
    ],
    "Person": [
        {"name": "name", "type": "string"},
        {"name": "wallet", "type": "address"}
    ],
    "Mail": [
        {"name": "from", "type": "Person"},
        {"name": "to", "type": "Person"},
        {"name": "contents", "type": "string"}
    ]
}

payload = json.dumps({
    "domain": domain_data,
    "types": types,
    "primaryType": "Mail",
    "message": message
})

sign_typed_data_result = client.invoke(
    uri=ethers_core_uri,
    method="signTypedData",
    args={"payload": payload}
)

print(f"Signed typed data: {sign_typed_data_result}")
assert sign_typed_data_result == "0x12bdd486cb42c3b3c414bb04253acfe7d402559e7637562987af6bd78508f38623c1cc09880613762cc913d49fd7d3c091be974c0dee83fb233300b6b58727311c"
```

## Conclusion

This example demonstrates how to use the `PolywrapClient` to interact with the Ethereum Network.
For more information on the `PolywrapClient`, please refer to the 
[Polywrap Python Client documentation](https://polywrap-client.rtfd.io).
