from typing import cast

import pytest
from polywrap_core import InvokeOptions, Uri
from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginWrapper
from polywrap_client import PolywrapClient
from polywrap_result import Ok

from test_plugin_module import GreetingModule 

@pytest.mark.asyncio
async def test_plugin_wrapper_invoke():
    module = GreetingModule({})
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