# polywrap-plugin

Python implementation of the plugin wrapper runtime.

## Usage

### Invoke Plugin Wrapper

```python
from typing import Any, Dict, List, Union, Optional
from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginModule
from polywrap_core import InvokerClient, Uri, InvokerOptions, UriPackageOrWrapper, Env

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
client: InvokerClient = ...

result = await wrapper.invoke(
    uri=Uri.from_str("ens/greeting.eth"),
    method="greeting",
    args=args,
    client=client
)
assert result, "Greetings from: Joe"
```
