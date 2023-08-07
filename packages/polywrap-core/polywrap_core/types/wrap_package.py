"""This module contains the IWrapPackage interface."""
from __future__ import annotations

from typing import Optional, Protocol

from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions

from .wrapper import Wrapper


class WrapPackage(Protocol):
    """Defines protocol for representing the package of a wrapper."""

    def create_wrapper(self) -> Wrapper:
        """Create a new wrapper instance from the wrapper package.

        Returns:
            Wrapper: The newly created wrapper instance.
        """
        ...

    def get_manifest(
        self, options: Optional[DeserializeManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest from the wrapper package.

        Args:
            options (DeserializeManifestOptions): The options for getting the manifest.

        Returns:
            AnyWrapManifest: The manifest of the wrapper.
        """
        ...


__all__ = ["WrapPackage"]
