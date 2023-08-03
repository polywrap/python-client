# polywrap-web3-config-bundle
This package contains the web3 configuration bundle for Polywrap Client.

## Bundled Wraps

| wrap | description |
| - | - |
| http | To make HTTP requests |
| ipfs_http_client | To add or retrieve items from IPFS |
| ipfs_resolver | To fetch wraps from IPFS |
| ethereum_provider | To perform ethereum RPC calls |
| ethereum-wrapper | A higher level API to perform ethereum operations (like etheres.js) |
| ens_text_record_resolver | To resolve URIs from ens text record |
| ens_ipfs_contenthash_resolver | To resolve URIs from ens content hash |
| ens_resolver | To resolve URIs from ens |

## Usage
```python
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_web3_config_bundle import get_web3_config

config = PolywrapClientConfigBuilder.add(get_web3_config()).build()
```
