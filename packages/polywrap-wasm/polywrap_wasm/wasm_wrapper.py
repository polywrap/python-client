"""This module contains the WasmWrapper class for invoking Wasm wrappers."""
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
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_result import Err, Ok, Result
from wasmtime import Instance, Store

from .errors import WasmAbortError
from .exports import WrapExports
from .instance import create_instance
from .types.state import State


class WasmWrapper(Wrapper):
    """WasmWrapper implements the Wrapper interface for Wasm wrappers.

    Attributes:
        file_reader: The file reader used to read the wrapper files.
        wasm_module: The Wasm module file of the wrapper.
        manifest: The manifest of the wrapper.
    """

    file_reader: IFileReader
    wasm_module: bytes
    manifest: AnyWrapManifest

    def __init__(
        self, file_reader: IFileReader, wasm_module: bytes, manifest: AnyWrapManifest
    ):
        """Initialize a new WasmWrapper instance."""
        self.file_reader = file_reader
        self.wasm_module = wasm_module
        self.manifest = manifest

    def get_manifest(self) -> Result[AnyWrapManifest]:
        """Get the manifest of the wrapper."""
        return Ok(self.manifest)

    def get_wasm_module(self) -> Result[bytes]:
        """Get the Wasm module of the wrapper."""
        return Ok(self.wasm_module)

    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        """Get a file from the wrapper.

        Args:
            options: The options to use when getting the file.

        Returns:
            The file contents as string or bytes according to encoding or an error.
        """
        result = await self.file_reader.read_file(options.path)
        if result.is_err():
            return cast(Err, result)
        data = result.unwrap()
        return Ok(data.decode(encoding=options.encoding) if options.encoding else data)

    def create_wasm_instance(
        self, store: Store, state: State, invoker: Invoker
    ) -> Union[Instance, None]:
        """Create a new Wasm instance for the wrapper.

        Args:
            store: The Wasm store to use when creating the instance.
            state: The Wasm wrapper state to use when creating the instance.
            invoker: The invoker to use when creating the instance.

        Returns:
            The Wasm instance of the wrapper Wasm module.
        """
        if self.wasm_module:
            return create_instance(store, self.wasm_module, state, invoker)
        return None

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        """Invoke the wrapper.

        Args:
            options: The options to use when invoking the wrapper.
            invoker: The invoker to use when invoking the wrapper.

        Returns:
            The result of the invocation or an error.
        """
        if not (options.uri and options.method):
            return Err.with_tb(
                ValueError(
                    dedent(
                        f"""
                    Expected invocation uri and method to be defiened got:
                    uri: {options.uri}
                    method: {options.method}
                    """
                    )
                )
            )

        state = State()
        state.uri = options.uri.uri
        state.method = options.method
        state.args = (
            options.args
            if isinstance(options.args, (bytes, bytearray))
            else msgpack_encode(options.args).unwrap()
        )
        state.env = (
            options.env
            if isinstance(options.env, (bytes, bytearray))
            else msgpack_encode(options.env).unwrap()
        )

        method_length = len(state.method)
        args_length = len(state.args)
        env_length = len(state.env)

        store = Store()
        instance = self.create_wasm_instance(store, state, invoker)
        if not instance:
            return Err.with_tb(
                WasmAbortError(
                    state.uri,
                    state.method,
                    msgpack_decode(state.args).unwrap() if state.args else None,
                    msgpack_decode(state.env).unwrap() if state.env else None,
                    "Unable to instantiate the wasm module",
                )
            )
        try:
            exports = WrapExports(instance, store)

            result = exports.__wrap_invoke__(method_length, args_length, env_length)
        except Exception as err:
            return Err(err)

        return self._process_invoke_result(state, result)

    @staticmethod
    def _process_invoke_result(state: State, result: bool) -> Result[InvocableResult]:
        if result and state.invoke_result and state.invoke_result.is_ok():
            return Ok(
                InvocableResult(result=state.invoke_result.unwrap(), encoded=True)
            )
        if not result and state.invoke_result and state.invoke_result.is_err():
            return cast(Err, state.invoke_result)
        return Err.with_tb(ValueError("Invoke result is missing"))
