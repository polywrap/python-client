"""This module contains the UriPackage type."""
from __future__ import annotations

from dataclasses import dataclass

from .uri import Uri
from .wrap_package import IWrapPackage


@dataclass(slots=True, kw_only=True)
class UriPackage:
    """UriPackage is a dataclass that contains a URI and a wrap package.

    Attributes:
        uri: The final URI of the wrap package.
        package: The wrap package.
    """

    uri: Uri
    package: IWrapPackage
