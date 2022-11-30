from pytest import fixture
from typing import Any, Dict, List, Union

from polywrap_plugin import PluginModule
from polywrap_core import Invoker, Uri, InvokerOptions
from polywrap_result import Result

@fixture
def invoker() -> Invoker:
    class MockInvoker(Invoker):
        async def invoke(self, options: InvokerOptions) -> Result[Any]:
            raise NotImplemented

        def get_implementations(self, uri: Uri) -> Result[Union[List[Uri], None]]:
            raise NotImplemented
    
    return MockInvoker()


@fixture
def greeting_module():
    class GreetingModule(PluginModule[None, str]):
        def __init__(self, config: None):
            super().__init__(config)

        def greeting(self, args: Dict[str, Any], client: Invoker):
            return f"Greetings from: {args['name']}"

    return GreetingModule(None)