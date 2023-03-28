"""This module contains the PluginModule class."""
# pylint: disable=invalid-name
from abc import ABC
from typing import Any, Generic, TypeVar

from polywrap_core import (
    InvokeOptions,
    Invoker,
    UriPackageOrWrapper,
    WrapAbortError,
    WrapInvocationError,
    execute_maybe_async_function,
)
from polywrap_msgpack import msgpack_decode

TConfig = TypeVar("TConfig")


class PluginModule(Generic[TConfig], ABC):
    """PluginModule is the base class for all plugin modules.

    Attributes:
        config: The configuration of the plugin.
    """

    config: TConfig

    def __init__(self, config: TConfig):
        """Initialize a new PluginModule instance.

        Args:
            config: The configuration of the plugin.
        """
        self.config = config

    async def __wrap_invoke__(
        self,
        options: InvokeOptions[UriPackageOrWrapper],
        invoker: Invoker[UriPackageOrWrapper],
    ) -> Any:
        """Invoke a method on the plugin.

        Args:
            method: The name of the method to invoke.
            args: The arguments to pass to the method.
            invoker: The invoker to use for subinvocations.

        Returns:
            The result of the plugin method invocation or an error.
        """
        if not hasattr(self, options.method):
            raise WrapInvocationError(
                options, f"{options.method} is not defined in plugin module"
            )

        callable_method = getattr(self, options.method)
        if callable(callable_method):
            try:
                decoded_args = (
                    msgpack_decode(options.args)
                    if isinstance(options.args, bytes)
                    else options.args
                )
                return await execute_maybe_async_function(
                    callable_method, decoded_args, invoker, options.env
                )
            except Exception as err:
                raise WrapAbortError(options, repr(err)) from err
        raise WrapInvocationError(
            options, f"{options.method} is not a callable method in plugin module"
        )
