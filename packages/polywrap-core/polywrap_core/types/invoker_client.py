"""This module contains the InvokerClient interface."""
from __future__ import annotations

from .invoke import Invoker
from .uri_resolver_handler import UriResolverHandler


class InvokerClient(Invoker, UriResolverHandler):
    """InvokerClient interface defines core set of functionalities\
        for resolving and invoking a wrapper."""
