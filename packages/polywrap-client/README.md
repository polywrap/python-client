# polywrap-client

Python implementation of the polywrap client.

## Usage

### Configure and Instantiate

Use the `polywrap-uri-resolvers` package to configure resolver and build config for the client.

```python
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader

config = ClientConfig(
    resolver=FsUriResolver(file_reader=SimpleFileReader())
)

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
options: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(
    uri=uri, method="method", args=args, encode_result=False
)
result = await client.invoke(options)
assert result == "123000"
```