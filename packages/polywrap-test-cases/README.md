# polywrap-wasm

Python implementation of the plugin wrapper runtime.

## Usage

### Invoke Plugin Wrapper

```python
from typing import Any, Dict, List, Union, Optional
from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginModule
from polywrap_core import Invoker, Uri, InvokerOptions, UriPackageOrWrapper, Env

class GreetingModule(PluginModule[None]):
    def __init__(self, config: None):
        super().__init__(config)

    def greeting(self, args: Dict[str, Any], client: Invoker[UriPackageOrWrapper], env: Optional[Env] = None):
        return f"Greetings from: {args['name']}"

manifest = cast(AnyWrapManifest, {})
wrapper = PluginWrapper(greeting_module, manifest)
args = {
    "name": "Joe"
}
options: InvokeOptions[UriPackageOrWrapper] = InvokeOptions(
    uri=Uri.from_str("ens/greeting.eth"),
    method="greeting",
    args=args
)
invoker: Invoker = ...

result = await wrapper.invoke(options, invoker)
assert result, "Greetings from: Joe"
```
