from typing import cast

import pytest
from polywrap_core import InvokeOptions, Uri, AnyWrapManifest, Invoker
from polywrap_plugin import PluginPackage, PluginModule
from polywrap_result import Ok

@pytest.mark.asyncio
async def test_plugin_package_invoke(greeting_module: PluginModule[None, str], invoker: Invoker):
    manifest = cast(AnyWrapManifest, {})
    plugin_package = PluginPackage(greeting_module, manifest)
    wrapper = (await plugin_package.create_wrapper()).unwrap()
    args = {
        "name": "Joe"
    }
    options = InvokeOptions(
        uri=Uri("ens/greeting.eth"),
        method="greeting",
        args=args
    )

    result = await wrapper.invoke(options, invoker)
    assert result, Ok("Greetings from: Joe")