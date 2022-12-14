"""
This file was automatically generated by scripts/templates/__init__.py.jinja2.
DO NOT MODIFY IT BY HAND. Instead, modify scripts/templates/__init__.py.jinja2,
and run python ./scripts/generate.py to regenerate this file.
"""

from dataclasses import dataclass
from enum import Enum

from .wrap_0_1 import Abi as WrapAbi_0_1_0_1
from .wrap_0_1 import WrapManifest as WrapManifest_0_1
from .wrap_0_1 import *


@dataclass(slots=True, kw_only=True)
class DeserializeManifestOptions:
    no_validate: Optional[bool] = None


@dataclass(slots=True, kw_only=True)
class serializeManifestOptions:
    no_validate: Optional[bool] = None


class WrapManifestVersions(Enum):
    VERSION_0_1 = "0.1", "0.1.0"

    def __new__(cls, value: int, *aliases: str) -> "WrapManifestVersions":
        obj = object.__new__(cls)
        obj._value_ = value
        for alias in aliases:
            cls._value2member_map_[alias] = obj
        return obj


class WrapManifestAbiVersions(Enum):
    VERSION_0_1 = "0.1"


class WrapAbiVersions(Enum):
    VERSION_0_1 = "0.1"


AnyWrapManifest = WrapManifest_0_1
AnyWrapAbi = WrapAbi_0_1_0_1


WrapManifest = WrapManifest_0_1
WrapAbi = WrapAbi_0_1_0_1

latest_wrap_manifest_version = "0.1"
latest_wrap_abi_version = "0.1"
