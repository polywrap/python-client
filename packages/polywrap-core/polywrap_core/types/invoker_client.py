"""This module contains the InvokerClient interface."""
from __future__ import annotations

from typing import Generic, TypeVar

from .invoker import Invoker
from .uri_like import UriLike
from .uri_resolver_handler import UriResolverHandler

T = TypeVar("T", bound=UriLike)


class InvokerClient(Generic[T], Invoker[T], UriResolverHandler[T]):
    """InvokerClient interface defines core set of functionalities\
        for resolving and invoking a wrapper."""
