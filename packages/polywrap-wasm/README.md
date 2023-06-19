# polywrap-wasm

Python implementation of the Wasm wrapper runtime.

## Usage

### Invoke Wasm Wrapper

```python
from typing import cast
from polywrap_manifest import AnyWrapManifest
from polywrap_core import FileReader, InvokerClient
from polywrap_wasm import WasmWrapper

file_reader: FileReader = ... # any valid file_reader, pass NotImplemented for mocking
wasm_module: bytes = bytes("<wrapper wasm module bytes read from file or http>")
wrap_manifest: AnyWrapManifest = ...
wrapper = WasmWrapper(file_reader, wasm_module, wrap_manifest)
client: InvokerClient = ... # any valid invoker client, mostly PolywrapClient

message = "hey"
args = {"arg": message}
result = wrapper.invoke(
  uri=Uri.from_str("fs/./build"),
  method="simpleMethod",
  args=args,
  client=client
)
assert result.encoded is True
assert msgpack_decode(cast(bytes, result.result)) == message
```
