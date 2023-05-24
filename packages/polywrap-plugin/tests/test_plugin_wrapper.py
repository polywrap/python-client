from typing import cast

from polywrap_core import Uri, Invoker
from polywrap_manifest import AnyWrapManifest

from polywrap_plugin import PluginWrapper, PluginModule


def test_plugin_wrapper_invoke(
    greeting_module: PluginModule[None], invoker: Invoker
):
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(greeting_module, manifest)
    args = {"name": "Joe"}

    result = wrapper.invoke(
        uri=Uri.from_str("ens/greeting.eth"),
        method="greeting",
        args=args,
        invoker=invoker,
    )
    assert result, "Greetings from: Joe"
