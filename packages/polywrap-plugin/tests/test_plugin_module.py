from typing import Any, Dict

import pytest
from polywrap_client import PolywrapClient
from polywrap_core import Invoker
from polywrap_result import Ok

from polywrap_plugin import PluginModule


class GreetingModule(PluginModule[Any, str]):
    def __init__(self, config: Any):
        super().__init__(config)

    def greeting(self, args: Dict[str, Any], client: Invoker):
        return f"Greetings from: {args['name']}"

@pytest.mark.asyncio
async def test_plugin_module():
    plugin = GreetingModule({})

    client = PolywrapClient()
    result = await plugin._wrap_invoke("greeting", { "name": "Joe" }, client) # type: ignore
    assert result, Ok("Greetings from: Joe")