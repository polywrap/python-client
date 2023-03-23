"""This module contains GetManifestOptions type."""
from __future__ import annotations

from dataclasses import dataclass

from polywrap_manifest import DeserializeManifestOptions


@dataclass(slots=True, kw_only=True)
class GetManifestOptions(DeserializeManifestOptions):
    """Options for getting a manifest from a wrapper."""
