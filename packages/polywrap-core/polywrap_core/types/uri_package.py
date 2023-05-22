"""This module contains the UriPackage type."""
from __future__ import annotations

from dataclasses import dataclass

from .uri import Uri
from .wrap_package import WrapPackage


@dataclass(slots=True, kw_only=True)
class UriPackage:
    """UriPackage is a dataclass that contains a URI and a package.

    Attributes:
        uri: The URI.
        package: The package.
    """

    uri: Uri
    package: WrapPackage


__all__ = ["UriPackage"]
