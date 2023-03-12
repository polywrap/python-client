"""This module contains the options for various client methods."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from polywrap_manifest import DeserializeManifestOptions


@dataclass(slots=True, kw_only=True)
class GetFileOptions:
    """Options for getting a file from a wrapper.

    Attributes:
        path: Path to the file.
        encoding: Encoding of the file.
    """

    path: str
    encoding: Optional[str] = "utf-8"


@dataclass(slots=True, kw_only=True)
class GetManifestOptions(DeserializeManifestOptions):
    """Options for getting a manifest from a wrapper."""
