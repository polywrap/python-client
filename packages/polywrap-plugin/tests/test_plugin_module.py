import pytest
from polywrap_core import Invoker, Uri, UriPackageOrWrapper, InvokeOptions
from polywrap_plugin import PluginModule


@pytest.mark.asyncio
async def test_plugin_module(
    greeting_module: PluginModule[None], invoker: Invoker[UriPackageOrWrapper]
):
    result = await greeting_module.__wrap_invoke__(
        InvokeOptions(
            uri=Uri.from_str("plugin/greeting"), method="greeting", args={"name": "Joe"}
        ),
        invoker,
    )
    assert result, "Greetings from: Joe"
