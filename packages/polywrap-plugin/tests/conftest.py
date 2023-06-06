from pytest import fixture
from typing import Any, Dict, List, Union, Optional

from polywrap_plugin import PluginModule
from polywrap_core import InvokerClient, Uri

@fixture
def client() -> InvokerClient:
    class MockInvoker(InvokerClient):
        async def invoke(self, *args: Any) -> Any:
            raise NotImplementedError()

        def get_implementations(self, *args: Any) -> Union[List[Uri], None]:
            raise NotImplementedError()
    
    return MockInvoker()


@fixture
def greeting_module():
    class GreetingModule(PluginModule[None]):
        def __init__(self, config: None):
            super().__init__(config)

        def greeting(self, args: Dict[str, Any], client: InvokerClient, env: Optional[Any] = None):
            return f"Greetings from: {args['name']}"

    return GreetingModule(None)