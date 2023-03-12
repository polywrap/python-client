"""This module contains the UriWrapper type."""
from __future__ import annotations

from dataclasses import dataclass

from .uri import Uri
from .wrapper import Wrapper


@dataclass(slots=True, kw_only=True)
class UriWrapper:
    """UriWrapper is a dataclass that contains a URI and a wrapper.

    Attributes:
        uri: The final URI of the wrapper.
        wrapper: The wrapper.
    """

    uri: Uri
    wrapper: Wrapper
