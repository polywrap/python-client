from typing import cast
import pytest
from polywrap_result import Ok, Result
from polywrap_core import Invoker
from polywrap_plugin import PluginModule

@pytest.mark.asyncio
async def test_plugin_module(greeting_module: PluginModule[None], invoker: Invoker):
    result = cast(Result[str], await greeting_module.__wrap_invoke__("greeting", { "name": "Joe" }, invoker))
    assert result, Ok("Greetings from: Joe")