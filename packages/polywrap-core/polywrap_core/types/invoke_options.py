"""This module defines the InvokeOptions protocol."""
from typing import Any, Optional, Protocol

from .uri import Uri
from .uri_resolution_context import UriResolutionContext


class InvokeOptions(Protocol):
    """InvokeOptions holds the options for an invocation."""

    @property
    def uri(self) -> Uri:
        """The URI of the wrapper."""
        ...

    @property
    def method(self) -> str:
        """The method to invoke."""
        ...

    @property
    def args(self) -> Any:
        """The arguments to pass to the method."""
        ...

    @property
    def env(self) -> Any:
        """The environment variables to set for the invocation."""
        ...

    @property
    def resolution_context(self) -> Optional[UriResolutionContext]:
        """A URI resolution context."""
        ...
