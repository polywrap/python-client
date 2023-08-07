"""This module contains the interface for invoking any invocables."""
# pylint: disable=too-many-arguments

from __future__ import annotations

from typing import Any, List, Optional, Protocol

from .uri import Uri
from .uri_resolution_context import UriResolutionContext


class Invoker(Protocol):
    """Invoker protocol defines the methods for invoking an invocable."""

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        encode_result: Optional[bool] = False,
    ) -> Any:
        """Invoke the Invocable based on the provided InvokerOptions.

        Args:
            uri (Uri): Uri of the Invocable
            method (str): Method to be executed
            args (Optional[Any]) : Arguments for the method, structured as a dictionary
            env (Optional[Any]): Override the client's config for all invokes within this invoke.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context
            encode_result (Optional[bool]): If True, the result will be encoded

        Returns:
            Any: invocation result.
        """
        ...

    def get_implementations(
        self, uri: Uri, apply_resolution: bool = True
    ) -> Optional[List[Uri]]:
        """Get implementations of an interface with its URI.

        Args:
            uri (Uri): URI of the interface.
            apply_resolution (bool): If True, apply resolution to the URI and interfaces.

        Returns:
            Optional[List[Uri]]: List of implementations or None if not found.
        """
        ...


__all__ = ["Invoker"]
