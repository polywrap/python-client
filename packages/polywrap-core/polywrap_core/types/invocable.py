"""This module contains the interface for invoking any invocables."""
# pylint: disable=too-many-arguments

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol

from .invoker import Invoker
from .uri import Uri
from .uri_resolution_context import UriResolutionContext


@dataclass(slots=True, kw_only=True)
class InvocableResult:
    """Result of a wrapper invocation.

    Args:
        result (Optional[Any]): Invocation result. The type of this value is \
            the return type of the method.
        encoded (Optional[bool]): It will be set true if result is encoded
    """

    result: Optional[Any] = None
    encoded: Optional[bool] = None


class Invocable(Protocol):
    """Invocable interface."""

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        invoker: Optional[Invoker] = None,
    ) -> InvocableResult:
        """Invoke the Wrapper based on the provided InvokeOptions.

        Args:
            uri (Uri): Uri of the wrapper
            method (str): Method to be executed
            args (Optional[Any]) : Arguments for the method, structured as a dictionary
            env (Optional[Any]): Override the client's config for all invokes within this invoke.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context
            invoker (Optional[Invoker]): The invoker instance requesting this invocation.\
                This invoker will be used for any subinvocation that may occur.

        Returns:
            InvocableResult: Result of the invocation.
        """
        ...


__all__ = ["Invocable", "InvocableResult"]
