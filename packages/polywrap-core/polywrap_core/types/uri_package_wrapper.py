"""UriPackageOrWrapper is a Union type alias for a URI, a package, or a wrapper."""
from __future__ import annotations

from typing import Union

from .uri import Uri
from .uri_package import UriPackage
from .uri_wrapper import UriWrapper

UriPackageOrWrapper = Union[
    Uri, UriWrapper["UriPackageOrWrapper"], UriPackage["UriPackageOrWrapper"]
]
