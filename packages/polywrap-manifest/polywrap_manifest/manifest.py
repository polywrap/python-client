# This file was automatically generated by scripts/templates/__init__.py.jinja2.
# DO NOT MODIFY IT BY HAND. Instead, modify scripts/templates/__init__.py.jinja2,
# and run python ./scripts/generate.py to regenerate this file.
"""This module contains the latest version of the wrap manifest and abi."""

from dataclasses import dataclass
from enum import Enum

from .wrap_0_1 import Abi as WrapAbi_0_1_0_1
from .wrap_0_1 import WrapManifest as WrapManifest_0_1
from .wrap_0_1 import *


@dataclass(slots=True, kw_only=True)
class DeserializeManifestOptions:
    """Options for deserializing a manifest from msgpack encoded bytes.

    Args:
        no_validate: If true, do not validate the manifest.
    """

    no_validate: Optional[bool] = None


class WrapManifestVersions(Enum):
    """The versions of the Wrap manifest."""

    VERSION_0_1 = "0.1", "0.1.0"

    def __new__(cls, value: int, *aliases: str) -> "WrapManifestVersions":
        """Override the default __new__ method to allow aliases for enum values."""
        obj = object.__new__(cls)
        obj._value_ = value
        for alias in aliases:
            cls._value2member_map_[alias] = obj
        return obj


class WrapManifestAbiVersions(Enum):
    """The versions of the abi for the given version of wrap manifest."""

    VERSION_0_1 = "0.1"


class WrapAbiVersions(Enum):
    """The versions of the Wrap abi."""

    VERSION_0_1 = "0.1"


AnyWrapManifest = WrapManifest_0_1
AnyWrapAbi = WrapAbi_0_1_0_1


WrapManifest = WrapManifest_0_1
WrapAbi = WrapAbi_0_1_0_1

LATEST_WRAP_MANIFEST_VERSION = "0.1"
LATEST_WRAP_ABI_VERSION = "0.1"

__all__ = [
    # Options
    "DeserializeManifestOptions",
    # Enums
    "WrapManifestVersions",
    "WrapManifestAbiVersions",
    "WrapAbiVersions",
    # Concrete Versions
    "WrapManifest_0_1",
    "WrapAbi_0_1_0_1",
    # Any Versions
    "AnyWrapManifest",
    "AnyWrapAbi",
    # Latest Versions
    "WrapManifest",
    "WrapAbi",
    # Latest Version constants
    "LATEST_WRAP_MANIFEST_VERSION",
    "LATEST_WRAP_ABI_VERSION",
]
