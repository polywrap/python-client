"""This module contains the IWrapPackage interface."""
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from polywrap_manifest import AnyWrapManifest

from .options import GetManifestOptions
from .uri_like import UriLike
from .wrapper import Wrapper

TUriLike = TypeVar("TUriLike", bound=UriLike)


class WrapPackage(ABC, Generic[TUriLike]):
    """Wrapper package interface."""

    @abstractmethod
    async def create_wrapper(self) -> Wrapper[TUriLike]:
        """Create a new wrapper instance from the wrapper package.

        Returns:
            Wrapper: The newly created wrapper instance.
        """

    @abstractmethod
    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest from the wrapper package.

        Args:
            options: The options for getting the manifest.

        Returns:
            AnyWrapManifest: The manifest of the wrapper.
        """
