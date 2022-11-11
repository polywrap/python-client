from typing import Any, cast

import pytest
from polywrap_core import InvokeOptions, Uri, AnyWrapManifest
from polywrap_plugin import PluginPackage, PluginModule
from polywrap_client import PolywrapClient
from polywrap_result import Ok

@pytest.mark.asyncio
async def test_plugin_package_invoke(get_greeting_module: PluginModule[None, str]):
    module = get_greeting_module
    manifest = cast(AnyWrapManifest, {})
    plugin_package = PluginPackage(module, manifest)
    wrapper = (await plugin_package.create_wrapper()).unwrap()
    args = {
        "name": "Joe"
    }
    options = InvokeOptions(
        uri=Uri("ens/greeting.eth"),
        method="greeting",
        args=args
    )

    client = PolywrapClient()
    result = await wrapper.invoke(options, client)
    assert result, Ok("Greetings from: Joe")