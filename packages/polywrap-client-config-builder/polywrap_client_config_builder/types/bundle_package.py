"""This module contains the type for the bundle package."""
from dataclasses import dataclass
from typing import Any, Optional

from polywrap_core import Uri, WrapPackage


@dataclass(slots=True, kw_only=True)
class BundlePackage:
    """A bundle item is a single item in a bundle."""

    uri: Uri
    package: Optional[WrapPackage] = None
    implements: Optional[list[Uri]] = None
    redirects_from: Optional[list[Uri]] = None
    env: Optional[Any] = None


__all__ = ["BundlePackage"]
