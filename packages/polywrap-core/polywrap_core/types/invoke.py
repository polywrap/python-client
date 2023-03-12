"""This module contains the interface for invoking a wrapper."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from polywrap_result import Result

from .env import Env
from .uri import Uri
from .uri_resolution_context import IUriResolutionContext


@dataclass(slots=True, kw_only=True)
class InvokeOptions:
    """Options required for a wrapper invocation.

    Args:
        uri: Uri of the wrapper
        method: Method to be executed
        args: Arguments for the method, structured as a dictionary
        config: Override the client's config for all invokes within this invoke.
        context_id: Invoke id used to track query context data set internally.
    """

    uri: Uri
    method: str
    args: Optional[Union[Dict[str, Any], bytes]] = field(default_factory=dict)
    env: Optional[Env] = None
    resolution_context: Optional["IUriResolutionContext"] = None


@dataclass(slots=True, kw_only=True)
class InvocableResult:
    """Result of a wrapper invocation.

    Args:
        data: Invoke result data. The type of this value is the return type of the method.
        encoded: It will be set true if result is encoded
    """

    result: Optional[Any] = None
    encoded: Optional[bool] = None


@dataclass(slots=True, kw_only=True)
class InvokerOptions(InvokeOptions):
    """Options for invoking a wrapper using an invoker.

    Attributes:
        encode_result: If true, the result will be encoded.
    """

    encode_result: Optional[bool] = False


class Invoker(ABC):
    """Invoker interface."""

    @abstractmethod
    async def invoke(self, options: InvokerOptions) -> Result[Any]:
        """Invoke the Wrapper based on the provided InvokerOptions.

        Args:
            options: InvokerOptions for this invocation.

        Returns:
            Result[Any]: Result of the invocation or error.
        """

    @abstractmethod
    def get_implementations(self, uri: Uri) -> Result[Union[List[Uri], None]]:
        """Get implementations of an interface with its URI.

        Args:
            uri: URI of the interface.

        Returns:
            Result[Union[List[Uri], None]]: List of implementations or None if not found.
        """


class Invocable(ABC):
    """Invocable interface."""

    @abstractmethod
    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        """Invoke the Wrapper based on the provided InvokeOptions.

        Args:
            options: InvokeOptions for this invocation.
            invoker: The invoker instance requesting this invocation.\
                This invoker will be used for any subinvocation that may occur.

        Returns:
            Result[InvocableResult]: Result of the invocation or error.
        """
