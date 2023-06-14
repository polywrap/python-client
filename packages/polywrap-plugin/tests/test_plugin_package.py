from typing import cast

from polywrap_core import Uri, InvokerClient
from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginPackage, PluginModule


def test_plugin_package_invoke(
    greeting_module: PluginModule[None], client: InvokerClient
):
    manifest = cast(AnyWrapManifest, {})
    plugin_package = PluginPackage(greeting_module, manifest)
    wrapper = plugin_package.create_wrapper()
    args = {"name": "Joe"}

    result = wrapper.invoke(
        uri=Uri.from_str("ens/greeting.eth"),
        method="greeting",
        args=args,
        client=client,
    )
    assert result, "Greetings from: Joe"


def test_plugin_package_get_manifest(
    greeting_module: PluginModule[None], client: InvokerClient
):
    manifest = cast(AnyWrapManifest, {})
    plugin_package = PluginPackage(greeting_module, manifest)
    
    assert plugin_package.get_manifest() is manifest
