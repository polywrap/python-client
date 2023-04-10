"""This module contains the interface for invoking any invocables."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from ..env import Env
from ..invoke_args import InvokeArgs
from ..uri import Uri
from ..uri_like import UriLike
from ..uri_resolution_context import IUriResolutionContext

TUriLike = TypeVar("TUriLike", bound=UriLike)


@dataclass(slots=True, kw_only=True)
class InvokeOptions(Generic[TUriLike]):
    """Options required for a wrapper invocation.

    Args:
        uri (Uri): Uri of the wrapper
        method (str): Method to be executed
        args (Optional[InvokeArgs]) : Arguments for the method, structured as a dictionary
        env (Optional[Env]): Override the client's config for all invokes within this invoke.
        resolution_context (Optional[IUriResolutionContext]): A URI resolution context
    """

    uri: Uri
    method: str
    args: Optional[InvokeArgs] = field(default_factory=dict)
    env: Optional[Env] = None
    resolution_context: Optional[IUriResolutionContext[TUriLike]] = None
