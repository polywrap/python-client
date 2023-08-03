# polywrap-sys-config-bundle
This package contains the system configuration bundle for Polywrap Client.

## Bundled Wraps

| wrap | description |
| - | - |
| http | To make HTTP requests |
| http_resolver | To resolve URIs from HTTP server |
| wrapscan_resolver | To resolve URIs from wrapscan.io |
| ipfs_http_client | To add or retrieve items from IPFS |
| ipfs_resolver | To fetch wraps from IPFS |
| github_resolver | To fetch wraps from github repo |
| file_system | To perform file system operations |
| file_system_resolver | To fetch wraps from File System |

## Usage
```python
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_sys_config_bundle import get_sys_config

config = PolywrapClientConfigBuilder.add(get_sys_config()).build()
```
