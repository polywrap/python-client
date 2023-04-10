"""This package contains custom msgpack extension types\
    defined in the WRAP standard."""
from __future__ import annotations

from enum import Enum

from .generic_map import *


class ExtensionTypes(Enum):
    """Wrap msgpack extension types."""

    GENERIC_MAP = 1


__all__ = ["ExtensionTypes", "GenericMap"]
