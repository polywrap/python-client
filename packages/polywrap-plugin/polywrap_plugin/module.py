"""This module contains the PluginModule class."""
# pylint: disable=invalid-name
from abc import ABC
from typing import Any, Dict, Generic, List, TypeVar, cast

from polywrap_core import Invoker, execute_maybe_async_function
from polywrap_result import Err, Ok, Result

TConfig = TypeVar("TConfig")
TResult = TypeVar("TResult")


class PluginModule(Generic[TConfig], ABC):
    """PluginModule is the base class for all plugin modules.

    Attributes:
        env: The environment variables of the plugin.
        config: The configuration of the plugin.
    """

    env: Dict[str, Any]
    config: TConfig

    def __init__(self, config: TConfig):
        """Initialize a new PluginModule instance.

        Args:
            config: The configuration of the plugin.
        """
        self.config = config

    def set_env(self, env: Dict[str, Any]) -> None:
        """Set the environment variables of the plugin.

        Args:
            env: The environment variables of the plugin.
        """
        self.env = env

    async def __wrap_invoke__(
        self, method: str, args: Dict[str, Any], invoker: Invoker
    ) -> Result[TResult]:
        """Invoke a method on the plugin.

        Args:
            method: The name of the method to invoke.
            args: The arguments to pass to the method.
            invoker: The invoker to use for subinvocations.

        Returns:
            The result of the plugin method invocation or an error.
        """
        methods: List[str] = [name for name in dir(self) if name == method]

        if not methods:
            return Err.with_tb(RuntimeError(f"{method} is not defined in plugin"))

        callable_method = getattr(self, method)
        if callable(callable_method):
            try:
                result = await execute_maybe_async_function(
                    callable_method, args, invoker
                )
                if isinstance(result, (Ok, Err)):
                    return cast(Result[TResult], result)
                return Ok(result)
            except Exception as e:
                return Err(e)
        return Err.with_tb(RuntimeError(f"{method} is an attribute, not a method"))
