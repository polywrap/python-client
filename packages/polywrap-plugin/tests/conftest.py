from pytest import fixture
from typing import Any, Dict

from polywrap_plugin import PluginModule
from polywrap_core import Invoker

@fixture
def get_greeting_module():
    class GreetingModule(PluginModule[None, str]):
        def __init__(self, config: None):
            super().__init__(config)

        def greeting(self, args: Dict[str, Any], client: Invoker):
            return f"Greetings from: {args['name']}"

    instance = GreetingModule(None)
    return instance