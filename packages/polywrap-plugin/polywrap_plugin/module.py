from abc import ABC
from typing import Any, Dict, Generic, List, TypeVar, cast

from polywrap_core import Invoker, execute_maybe_async_function
from polywrap_result import Err, Ok, Result

TConfig = TypeVar("TConfig")
TResult = TypeVar("TResult")


class PluginModule(Generic[TConfig], ABC):
    env: Dict[str, Any]
    config: TConfig

    def __init__(self, config: TConfig):
        self.config = config

    def set_env(self, env: Dict[str, Any]) -> None:
        self.env = env

    async def __wrap_invoke__(
        self, method: str, args: Dict[str, Any], client: Invoker
    ) -> Result[TResult]:
        methods: List[str] = [name for name in dir(self) if name == method]

        if not methods:
            return Err.from_str(f"{method} is not defined in plugin")

        callable_method = getattr(self, method)
        if callable(callable_method):
            try:
                result = await execute_maybe_async_function(
                    callable_method, args, client
                )
                if isinstance(result, (Ok, Err)):
                    return cast(Result[TResult], result)
                return Ok(result)
            except Exception as e:
                return Err(e)
        return Err.from_str(f"{method} is an attribute, not a method")
