"""This module contains the PluginPackage class."""
# pylint: disable=invalid-name
from typing import Generic, Optional, TypeVar

from polywrap_core import GetManifestOptions, IWrapPackage, Wrapper
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Ok, Result

from .module import PluginModule
from .wrapper import PluginWrapper

TConfig = TypeVar("TConfig")


class PluginPackage(Generic[TConfig], IWrapPackage):
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

    async def create_wrapper(self) -> Result[Wrapper]:
        """Create a new plugin wrapper instance."""
        return Ok(PluginWrapper(module=self.module, manifest=self.manifest))

    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        """Get the manifest of the plugin.

        Args:
            options: The options to use when getting the manifest.

        Returns:
            The manifest of the plugin.
        """
        return Ok(self.manifest)
