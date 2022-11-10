from polywrap_core import IWrapPackage
from polywrap_manifest import AnyWrapManifest
from polywrap_plugin import PluginModule

class PluginPackage(IWrapPackage):
    module: PluginModule
    manifest: AnyWrapManifest

    def __init__(
        self, 
        module: PluginModule,
        manifest: AnyWrapManifest
    ):
        self.module = module
        self.manifest = manifest