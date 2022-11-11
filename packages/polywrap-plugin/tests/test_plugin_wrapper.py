from typing import cast, Callable, Any

import pytest
from polywrap_core import InvokeOptions, Uri
from polywrap_manifest import AnyWrapManifest
from polywrap_client import PolywrapClient
from polywrap_result import Ok

from polywrap_plugin import PluginWrapper, PluginModule

@pytest.mark.asyncio
async def test_plugin_wrapper_invoke(get_greeting_module: PluginModule[None, str]):
    module = get_greeting_module
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(module, manifest)
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