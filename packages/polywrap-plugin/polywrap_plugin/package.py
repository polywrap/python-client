from typing import Generic

from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginModule, TConfig, TResult

class PluginPackage(Generic[TConfig, TResult]):
    module: PluginModule[TConfig, TResult]
    manifest: AnyWrapManifest

    def __init__(
        self, 
        module: PluginModule[TConfig, TResult],
        manifest: AnyWrapManifest
    ):
        self.module = module
        self.manifest = manifest

