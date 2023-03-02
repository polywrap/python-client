from typing import cast

import pytest
from polywrap_core import InvokeOptions, Uri, Invoker
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Ok

from polywrap_plugin import PluginWrapper, PluginModule

@pytest.mark.asyncio
async def test_plugin_wrapper_invoke(greeting_module: PluginModule[None], invoker: Invoker):
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(greeting_module, manifest)
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