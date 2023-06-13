"""This module contains the PluginPackage class."""
# pylint: disable=invalid-name
from typing import Generic, Optional, TypeVar

from polywrap_core import WrapPackage, Wrapper
from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions

from .module import PluginModule
from .wrapper import PluginWrapper

TConfig = TypeVar("TConfig")


class PluginPackage(WrapPackage, Generic[TConfig]):
    """PluginPackage implements IWrapPackage interface for the plugin.

    Args:
        module (PluginModule[TConfig]): The plugin module.
        manifest (AnyWrapManifest): The manifest of the plugin.
    """

    module: PluginModule[TConfig]
    manifest: AnyWrapManifest

    def __init__(self, module: PluginModule[TConfig], manifest: AnyWrapManifest):
        """Initialize a new PluginPackage instance."""
        self.module = module
        self.manifest = manifest

    def create_wrapper(self) -> Wrapper:
        """Create a new plugin wrapper instance."""
        return PluginWrapper(module=self.module, manifest=self.manifest)

    def get_manifest(
        self, options: Optional[DeserializeManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest of the plugin.

        Args:
            options: The options to use when getting the manifest.

        Returns:
            The manifest of the plugin.
        """
        return self.manifest


__all__ = ["PluginPackage"]
