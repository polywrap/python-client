from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from result import Result

from .uri import Uri
from .uri_resolution_context import IUriResolutionContext


@dataclass(slots=True, kw_only=True)
class InvokeOptions:
    """
    Options required for a wrapper invocation.

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
    env: Optional[Dict[str, Any]] = None
    resolution_context: Optional[IUriResolutionContext] = None


@dataclass(slots=True, kw_only=True)
class InvokeResult:
    """
    Result of a wrapper invocation

    Args:
        data: Invoke result data. The type of this value is the return type of the method.
        error: Error encountered during the invocation.
    """

    result: Optional[Any] = None
    error: Optional[Exception] = None


@dataclass(slots=True, kw_only=True)
class InvokerOptions(InvokeOptions):
    encode_result: Optional[bool] = False


@dataclass(slots=True, kw_only=True)
class InvocableResult(InvokeResult):
    encoded: Optional[bool] = False


class Invoker(ABC):
    @abstractmethod
    async def invoke(self, options: InvokerOptions) -> InvokeResult:
        pass

    @abstractmethod
    def get_implementations(self, uri: Uri) -> Result[List[Uri], Exception]:
        pass


class Invocable(ABC):
    @abstractmethod
    async def invoke(self, options: InvokeOptions, invoker: Invoker) -> InvocableResult:
        pass
