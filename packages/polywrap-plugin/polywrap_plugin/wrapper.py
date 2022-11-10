from typing import Union, Any, Dict

from polywrap_core import Wrapper, InvokeOptions, Invoker, InvocableResult, GetFileOptions
from polywrap_plugin import PluginModule
from polywrap_result import Result, Ok, Err
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode

class PluginWrapper(Wrapper):
    manifest: AnyWrapManifest
    module: PluginModule

    def __init__(self, manifest: AnyWrapManifest, module: PluginModule) -> None:
        self.manifest = manifest
        self.module = module

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:

        method = options.method
        if not self.module.get_method(method):
            return Err(Exception(f"PluginWrapper: method {method} not found"))

        env = options.env if options.env else {}
        self.module.set_env(env)

        decoded_args: Dict[str, Any] = options.args if options.args else {}

        if isinstance(decoded_args, bytes):
            decoded_args = msgpack_decode(decoded_args)

        result = self.module._wrap_invoke(method, decoded_args, invoker)

        if result.ok:
            return Ok(InvocableResult(result=result,encoded=False))

        


    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        return Err(Exception("client.get_file(..) is not implemented for plugins"))

    def get_manifest(self) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)