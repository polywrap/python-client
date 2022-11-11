from abc import ABC
from typing import Any, Dict, TypeVar, Generic, List
import inspect

from polywrap_core import Invoker
from polywrap_result import Err, Ok

TConfig = TypeVar('TConfig')

class PluginModule(Generic[TConfig], ABC):
    env: Dict[str, Any]
    config: TConfig

    def __init__(self, config: TConfig):
        self.config = config

    def set_env(self, env: Dict[str, Any]) -> None:
        self.env = env

    async def _wrap_invoke(self, method: str, args: Dict[str, Any], client: Invoker):
        callable_method = self.get_method(method)      
        if not method:
            return Err(Exception(f"Plugin missing method {method}"))

        result = callable_method(args, client)
        print(result)
        return result

    def get_method(self, method: str):
        methods: List[str] = [name for name in dir(self) if name == method]
        callable_method = getattr(self, methods[0])

        # TODO: Change this to return Err instead of throwin
        if not callable(callable_method):
            raise Exception(f"Method {method} is an attribute, not a method")
        
        return callable_method
