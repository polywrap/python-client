from pytest import fixture
from typing import Any, Dict, List, Union, Optional

from polywrap_plugin import PluginModule
from polywrap_core import Invoker, Uri, InvokerOptions, UriPackageOrWrapper, Env

@fixture
def invoker() -> Invoker[UriPackageOrWrapper]:
    class MockInvoker(Invoker[UriPackageOrWrapper]):
        async def invoke(self, options: InvokerOptions[UriPackageOrWrapper]) -> Any:
            raise NotImplementedError()

        def get_implementations(self, uri: Uri) -> Union[List[Uri], None]:
            raise NotImplementedError()
    
    return MockInvoker()


@fixture
def greeting_module():
    class GreetingModule(PluginModule[None]):
        def __init__(self, config: None):
            super().__init__(config)

        def greeting(self, args: Dict[str, Any], client: Invoker[UriPackageOrWrapper], env: Optional[Env] = None):
            return f"Greetings from: {args['name']}"

    return GreetingModule(None)