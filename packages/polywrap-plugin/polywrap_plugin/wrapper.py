from typing import Any, Dict, Union, cast, Generic

from polywrap_core import (
    GetFileOptions,
    InvocableResult,
    InvokeOptions,
    Invoker,
    Wrapper
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode
from polywrap_result import Err, Ok, Result

from .module import PluginModule, TConfig, TResult

class PluginWrapper(Wrapper, Generic[TConfig, TResult]):
    module: PluginModule[TConfig, TResult]

    def __init__(self, module: PluginModule[TConfig, TResult], manifest: AnyWrapManifest) -> None:
        self.module = module
        self.manifest = manifest

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        env = options.env if options.env else {}
        self.module.set_env(env)

        decoded_args: Union[Dict[str, Any], bytes] = options.args if options.args else {}

        if isinstance(decoded_args, bytes):
            decoded_args = msgpack_decode(decoded_args)

        result: Result[TResult] = await self.module._wrap_invoke(options.method, decoded_args, invoker) # type: ignore

        if result.is_err():
            return cast(Err, result.err)

        return Ok(InvocableResult(result=result,encoded=False))


    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        return Err(Exception("client.get_file(..) is not implemented for plugins"))

    def get_manifest(self) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)