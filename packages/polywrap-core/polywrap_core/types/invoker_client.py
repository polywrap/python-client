"""This module contains the InvokerClient interface."""
from __future__ import annotations

from typing import Protocol

from .invoker import Invoker
from .uri_resolver_handler import UriResolverHandler


class InvokerClient(Invoker, UriResolverHandler, Protocol):
    """InvokerClient protocol defines core set of functionalities\
        for resolving and invoking an Invocable."""


__all__ = ["InvokerClient"]
