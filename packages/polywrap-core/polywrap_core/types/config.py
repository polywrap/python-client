"""This module contains the ClientConfig type."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .uri import Uri
from .uri_resolver import UriResolver


@dataclass(slots=True, kw_only=True)
class ClientConfig:
    """Defines Client configuration dataclass.

    Args:
        envs (Dict[Uri, Any]): Dictionary of environments \
            where key is URI and value is env.
        interfaces (Dict[Uri, List[Uri]]): Dictionary of interfaces \
            and their implementations where key is interface URI \
            and value is list of implementation URIs.
        resolver (UriResolver): URI resolver.
    """

    envs: Dict[Uri, Any] = field(default_factory=dict)
    interfaces: Dict[Uri, List[Uri]] = field(default_factory=dict)
    resolver: UriResolver


__all__ = ["ClientConfig"]
