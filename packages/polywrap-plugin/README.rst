Polywrap Plugin
===============
This package contains the runtime for the Polywrap plugin system.

Quickstart
----------

Imports
~~~~~~~

>>> from typing import Any, Dict, List, Union, Optional, cast
>>> from polywrap_manifest import AnyWrapManifest
>>> from polywrap_plugin import PluginModule
>>> from polywrap_core import InvokerClient, Uri

Define a plugin module
~~~~~~~~~~~~~~~~~~~~~~

>>> class GreetingModule(PluginModule[None]):
...     def __init__(self, config: None):
...         super().__init__(config)
...
...     def greeting(self, args: Dict[str, Any], client: InvokerClient, env: Optional[Any] = None):
...         return f"Greetings from: {args['name']}"

Create a plugin wrapper
~~~~~~~~~~~~~~~~~~~~~~~

>>> greeting_module = GreetingModule(None)
>>> manifest = cast(AnyWrapManifest, NotImplemented)
>>> wrapper = PluginWrapper(greeting_module, manifest)

Invocation
~~~~~~~~~~

>>> args = {
...     "name": "Joe"
... }
>>> result = wrapper.invoke(
...     uri=Uri.from_str("ens/greeting.eth"),
...     method="greeting",
...     args=args,
...     client=cast(InvokerClient, NotImplemented),
... )
>>> assert result.result == "Greetings from: Joe"
