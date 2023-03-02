from typing import Generic, Optional, TypeVar

from polywrap_core import GetManifestOptions, IWrapPackage, Wrapper
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Ok, Result

from .module import PluginModule
from .wrapper import PluginWrapper

TConfig = TypeVar("TConfig")


class PluginPackage(Generic[TConfig], IWrapPackage):
    module: PluginModule[TConfig]
    manifest: AnyWrapManifest

    def __init__(self, module: PluginModule[TConfig], manifest: AnyWrapManifest):
        self.module = module
        self.manifest = manifest

    async def create_wrapper(self) -> Result[Wrapper]:
        return Ok(PluginWrapper(module=self.module, manifest=self.manifest))

    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)
