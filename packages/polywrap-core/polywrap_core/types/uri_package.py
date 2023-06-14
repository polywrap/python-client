"""This module contains the UriPackage type."""
from __future__ import annotations

from dataclasses import dataclass

from .uri import Uri
from .wrap_package import WrapPackage


@dataclass(slots=True, kw_only=True)
class UriPackage:
    """UriPackage is a dataclass that contains a URI and a package.

    Args:
        uri (Uri): The URI of the wrap package.
        package (WrapPackage): The wrap package.
    """

    uri: Uri
    """The URI of the wrap package."""

    package: WrapPackage
    """The wrap package."""


__all__ = ["UriPackage"]
