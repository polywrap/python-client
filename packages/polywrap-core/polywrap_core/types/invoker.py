"""This module contains the interface for invoking any invocables."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, TypeVar, Union

from .options.invoke_options import InvokeOptions
from .uri import Uri
from .uri_like import UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


@dataclass(slots=True, kw_only=True)
class InvokerOptions(Generic[TUriLike], InvokeOptions[TUriLike]):
    """Options for invoking a wrapper using an invoker.

    Attributes:
        encode_result (Optional[bool]): If true, the result will be encoded.
    """

    encode_result: Optional[bool] = False


class Invoker(ABC, Generic[TUriLike]):
    """Invoker interface defines the methods for invoking a wrapper."""

    @abstractmethod
    async def invoke(self, options: InvokerOptions[TUriLike]) -> Any:
        """Invoke the Wrapper based on the provided InvokerOptions.

        Args:
            options (InvokerOptions): InvokerOptions for this invocation.

        Returns:
            Any: invocation result.
        """

    @abstractmethod
    def get_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        """Get implementations of an interface with its URI.

        Args:
            uri (Uri): URI of the interface.

        Returns:
            Union[List[Uri], None]: List of implementations or None if not found.
        """
