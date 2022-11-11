from typing import TypeVar, Dict, Any

import pytest
from polywrap_client import PolywrapClient
from polywrap_core import Invoker

from polywrap_plugin import PluginModule

TConfig = TypeVar('TConfig')

class GreetingModule(PluginModule):
    def __init__(self, config: TConfig):
        super().__init__(config)

    def greeting(self, args: Dict[str, Any], client: Invoker):
        return f"Greetings from: {args['name']}"

@pytest.mark.asyncio
async def test_plugin_module():
    plugin = GreetingModule({})

    client = PolywrapClient()
    result = await plugin._wrap_invoke("greeting", { "name": "Joe" }, client)
    print(result)
    assert result, "Greetings from: Joe"