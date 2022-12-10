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
    env: Optional[Env] = None
    resolution_context: Optional[IUriResolutionContext] = None


@dataclass(slots=True, kw_only=True)
class InvocableResult:
    """
    Result of a wrapper invocation

    Args:
        data: Invoke result data. The type of this value is the return type of the method.
        encoded: It will be set true if result is encoded
    """

    result: Optional[Any] = None
    encoded: Optional[bool] = None


@dataclass(slots=True, kw_only=True)
class InvokerOptions(InvokeOptions):
    encode_result: Optional[bool] = False


class Invoker(ABC):
    @abstractmethod
    async def invoke(self, options: InvokerOptions) -> Result[Any]:
        pass

    @abstractmethod
    def get_implementations(self, uri: Uri) -> Result[Union[List[Uri], None]]:
        pass


class Invocable(ABC):
    @abstractmethod
    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        pass
