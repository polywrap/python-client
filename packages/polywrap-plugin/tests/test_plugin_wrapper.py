from typing import cast

import pytest
from polywrap_core import InvokeOptions, Uri, Invoker, UriPackageOrWrapper
from polywrap_manifest import AnyWrapManifest

from polywrap_plugin import PluginWrapper, PluginModule

@pytest.mark.asyncio
async def test_plugin_wrapper_invoke(greeting_module: PluginModule[None], invoker: Invoker[UriPackageOrWrapper]):
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

    result = await wrapper.invoke(options, invoker)
    assert result, "Greetings from: Joe"