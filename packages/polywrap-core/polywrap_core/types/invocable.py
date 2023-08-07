"""This module contains the interface for invoking any invocables."""
# pylint: disable=too-many-arguments

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol

from .invoker_client import InvokerClient
from .uri import Uri
from .uri_resolution_context import UriResolutionContext


@dataclass(slots=True, kw_only=True)
class InvocableResult:
    """Result of an Invocable invocation.

    Args:
        result (Any): Invocation result. The type of this value is \
            the return type of the method.
        encoded (Optional[bool]): It will be set true if result is encoded
    """

    result: Any
    encoded: Optional[bool] = None


class Invocable(Protocol):
    """Defines Protocol for an Invocable that can be invoked by an invoker."""

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        client: Optional[InvokerClient] = None,
    ) -> InvocableResult:
        """Invoke the Invocable based on the provided InvokeOptions.

        Args:
            uri (Uri): Uri of the Invocable
            method (str): Method to be executed
            args (Optional[Any]) : Arguments for the method, structured as a dictionary
            env (Optional[Any]): Override the client's config for all invokes within this invoke.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context
            client (Optional[InvokerClient]): The invoker client instance requesting\
                this invocation. This invoker client will be used for any subinvocation\
                that may occur.

        Returns:
            InvocableResult: Result of the invocation.
        """
        ...


__all__ = ["Invocable", "InvocableResult"]
