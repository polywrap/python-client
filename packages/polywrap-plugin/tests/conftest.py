from pytest import fixture
from typing import Any, Dict

from polywrap_plugin import PluginModule
from polywrap_core import Invoker

@fixture
def get_greeting_module():
    class GreetingModule(PluginModule[Any, str]):
        def __init__(self, config: Any):
            super().__init__(config)

        def greeting(self, args: Dict[str, Any], client: Invoker):
            return f"Greetings from: {args['name']}"

    instance = GreetingModule({})
    return instance