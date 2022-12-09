from textwrap import dedent
from typing import Union, cast

from polywrap_core import (
    GetFileOptions,
    IFileReader,
    InvocableResult,
    InvokeOptions,
    Invoker,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_encode
from polywrap_result import Err, Ok, Result
from wasmtime import Store

from .exports import WrapExports
from .imports import create_instance
from .types.state import State


class WasmWrapper(Wrapper):
    file_reader: IFileReader
    wasm_module: bytes
    manifest: AnyWrapManifest

    def __init__(
        self, file_reader: IFileReader, wasm_module: bytes, manifest: AnyWrapManifest
    ):
        self.file_reader = file_reader
        self.wasm_module = wasm_module
        self.manifest = manifest

    def get_manifest(self) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)

    def get_wasm_module(self) -> Result[bytes]:
        return Ok(self.wasm_module)

    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        result = await self.file_reader.read_file(options.path)
        if result.is_err():
            return cast(Err, result)
        data = result.unwrap()
        return Ok(data.decode(encoding=options.encoding) if options.encoding else data)

    def create_wasm_instance(self, store: Store, state: State, invoker: Invoker):
        if self.wasm_module:
            return create_instance(store, self.wasm_module, state, invoker)

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        state = State()
        state.method = options.method
        state.args = (
            options.args
            if isinstance(options.args, (bytes, bytearray))
            else msgpack_encode(options.args)
        )
        state.env = (
            options.env
            if isinstance(options.env, (bytes, bytearray))
            else msgpack_encode(options.env)
        )

        if not (state.method and state.args and state.env):
            raise ValueError(
                dedent(
                    """
                    Expected invocation state to be definied got:
                    method: ${state.method}
                    args: ${state.args}
                    env: ${state.env}
                    """
                )
            )

        method_length = len(state.method)
        args_length = len(state.args)
        env_length = len(state.env)

        store = Store()
        instance = self.create_wasm_instance(store, state, invoker)
        if not instance:
            raise RuntimeError("Unable to instantiate the wasm module")
        exports = WrapExports(instance, store)

        result = exports.__wrap_invoke__(method_length, args_length, env_length)
        return self._process_invoke_result(state, result)

    @staticmethod
    def _process_invoke_result(state: State, result: bool) -> Result[InvocableResult]:
        if result and state.invoke["result"]:
            return Ok(InvocableResult(result=state.invoke["result"], encoded=True))
        elif result or not state.invoke["error"]:
            return Err.from_str("Invoke result is missing")
        else:
            return Err.from_str(state.invoke["error"])
