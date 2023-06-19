# polywrap-client

Python implementation of the polywrap client.

## Usage

### Configure and Instantiate

Use the `polywrap-uri-resolvers` package to configure resolver and build config for the client.

```python
from polywrap_uri_resolvers import (
    FsUriResolver,
    SimpleFileReader
)
from polywrap_core import Uri, ClientConfig
from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder

builder = (
    PolywrapClientConfigBuilder()
    .add_resolver(FsUriResolver(file_reader=SimpleFileReader()))
    .set_env(Uri.from_str("ens/foo.eth"), {"foo": "bar"})
    .add_interface_implementations(
        Uri.from_str("ens/foo.eth"), [
            Uri.from_str("ens/bar.eth"),
            Uri.from_str("ens/baz.eth")
        ]
    )
)
config = builder.build()
client = PolywrapClient(config)
```

### Invoke

Invoke a wrapper.

```python
uri = Uri.from_str(
    'fs/<path to wrapper>'  # Example uses simple math wrapper
)
args = {
    "arg1": "123",  # The base number
    "obj": {
        "prop1": "1000",  # multiply the base number by this factor
    },
}
result = client.invoke(uri=uri, method="method", args=args, encode_result=False)
assert result == "123000"
```