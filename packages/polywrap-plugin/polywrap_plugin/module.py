"""This module contains the PluginModule class."""
# pylint: disable=invalid-name
from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from polywrap_core import (
    InvokerClient,
    Uri,
    UriResolutionContext,
    WrapAbortError,
    WrapInvocationError,
)
from polywrap_msgpack import msgpack_decode

TConfig = TypeVar("TConfig")


@dataclass(kw_only=True, slots=True)
class PluginInvokeOptions:
    """PluginInvokeOptions is a dataclass that holds the options for an invocation.

    Args:
        uri (URI): The URI of the wrapper.
        method (str): The method to invoke.
        args (Optional[Any]): The arguments to pass to the method.
        env (Optional[Any]): The environment variables to set\
            for the invocation.
        resolution_context (Optional[UriResolutionContext]): \
            A URI resolution context.
        client (Optional[InvokerClient]): The client to use\
            for subinvocations.
    """

    uri: Uri
    method: str
    args: Optional[Any] = None
    env: Optional[Any] = None
    resolution_context: Optional[UriResolutionContext] = None
    client: Optional[InvokerClient] = None


class PluginModule(Generic[TConfig], ABC):
    """PluginModule is the base class for all plugin modules.

    Args:
        config (TConfig): The configuration of the plugin.
    """

    config: TConfig

    def __init__(self, config: TConfig):
        """Initialize a new PluginModule instance."""
        self.config = config

    def __wrap_invoke__(
        self,
        options: PluginInvokeOptions,
    ) -> Any:
        """Invoke a method on the plugin.

        Args:
            options (PluginInvokeOptions): The options\
                to use when invoking the plugin.

        Returns:
            The result of the plugin method invocation.

        Raises:
            WrapInvocationError: If the plugin method is not defined\
                or is not callable.
            WrapAbortError: If the plugin method raises an exception.
            MsgpackDecodeError: If the plugin method returns invalid msgpack.
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
                return callable_method(decoded_args, options.client, options.env)
            except Exception as err:
                raise WrapAbortError(options, repr(err)) from err
        raise WrapInvocationError(
            options, f"{options.method} is not a callable method in plugin module"
        )


__all__ = ["PluginModule"]
