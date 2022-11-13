from typing import Any

import pytest
from polywrap_client import PolywrapClient
from polywrap_result import Ok

from polywrap_plugin import PluginModule

@pytest.mark.asyncio
async def test_plugin_module(get_greeting_module: PluginModule[None, str]):
    module = get_greeting_module

    client = PolywrapClient()
    result = await module.__wrap_invoke__("greeting", { "name": "Joe" }, client)
    assert result, Ok("Greetings from: Joe")