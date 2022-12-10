from typing import Any, Dict, Generic, Union, cast

from polywrap_core import (
    GetFileOptions,
    InvocableResult,
    InvokeOptions,
    Invoker,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode
from polywrap_result import Err, Ok, Result

from .module import PluginModule, TConfig, TResult


class PluginWrapper(Wrapper, Generic[TConfig, TResult]):
    module: PluginModule[TConfig, TResult]

    def __init__(
        self, module: PluginModule[TConfig, TResult], manifest: AnyWrapManifest
    ) -> None:
        self.module = module
        self.manifest = manifest

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        env = options.env or {}
        self.module.set_env(env)

        args: Union[Dict[str, Any], bytes] = options.args or {}
        decoded_args: Dict[str, Any] = (
            msgpack_decode(args) if isinstance(args, bytes) else args
        )

        result: Result[TResult] = await self.module.__wrap_invoke__(
            options.method, decoded_args, invoker
        )

        if result.is_err():
            return cast(Err, result.err)
        return Ok(InvocableResult(result=result.unwrap(), encoded=False))

    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        return Err.from_str("client.get_file(..) is not implemented for plugins")

    def get_manifest(self) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)
