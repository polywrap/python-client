from polywrap_core import Invoker, Uri
from polywrap_plugin import PluginModule
from polywrap_plugin.module import InvokeOptions


def test_plugin_module(
    greeting_module: PluginModule[None], invoker: Invoker
):
    result = greeting_module.__wrap_invoke__(
        InvokeOptions(
            uri=Uri.from_str("plugin/greeting"), method="greeting", args={"name": "Joe"}, invoker=invoker
        ),
    )
    assert result, "Greetings from: Joe"
