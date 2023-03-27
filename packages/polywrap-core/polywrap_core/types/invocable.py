"""This module contains the interface for invoking any invocables."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from .invoker import Invoker
from .options.invoke_options import InvokeOptions
from .uri_like import UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


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


class Invocable(ABC, Generic[TUriLike]):
    """Invocable interface."""

    @abstractmethod
    async def invoke(
        self, options: InvokeOptions[TUriLike], invoker: Invoker[TUriLike]
    ) -> InvocableResult:
        """Invoke the Wrapper based on the provided InvokeOptions.

        Args:
            options (InvokeOptions): InvokeOptions for this invocation.
            invoker (Invoker): The invoker instance requesting this invocation.\
                This invoker will be used for any subinvocation that may occur.

        Returns:
            InvocableResult: Result of the invocation.
        """
