"""This module contains the IWrapPackage interface."""
from abc import ABC, abstractmethod
from typing import Optional

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .options import GetManifestOptions
from .wrapper import Wrapper


class IWrapPackage(ABC):
    """Wrapper package interface."""

    @abstractmethod
    async def create_wrapper(self) -> Result[Wrapper]:
        """Create a wrapper from the wrapper package.

        Returns:
            Result[Wrapper]: The wrapper or an error.
        """

    @abstractmethod
    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        """Get the manifest from the wrapper package.

        Args:
            options: The options for getting the manifest.

        Returns:
            Result[AnyWrapManifest]: The manifest or an error.
        """
