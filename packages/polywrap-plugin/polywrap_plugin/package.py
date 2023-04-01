"""This module contains the PluginPackage class."""
# pylint: disable=invalid-name
from typing import Generic, Optional, TypeVar

from polywrap_core import GetManifestOptions, UriPackageOrWrapper, WrapPackage, Wrapper
from polywrap_manifest import AnyWrapManifest

from .module import PluginModule
from .wrapper import PluginWrapper

TConfig = TypeVar("TConfig")


class PluginPackage(Generic[TConfig], WrapPackage[UriPackageOrWrapper]):
    """PluginPackage implements IWrapPackage interface for the plugin.

    Attributes:
        module: The plugin module.
        manifest: The manifest of the plugin.
    """

    module: PluginModule[TConfig]
    manifest: AnyWrapManifest

    def __init__(self, module: PluginModule[TConfig], manifest: AnyWrapManifest):
        """Initialize a new PluginPackage instance.

        Args:
            module: The plugin module.
            manifest: The manifest of the plugin.
        """
        self.module = module
        self.manifest = manifest

    async def create_wrapper(self) -> Wrapper[UriPackageOrWrapper]:
        """Create a new plugin wrapper instance."""
        return PluginWrapper(module=self.module, manifest=self.manifest)

    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest of the plugin.

        Args:
            options: The options to use when getting the manifest.

        Returns:
            The manifest of the plugin.
        """
        return self.manifest
