"""This module contains the WasmWrapper class for invoking Wasm wrappers."""
from textwrap import dedent
from typing import Union

from polywrap_core import (
    FileReader,
    GetFileOptions,
    InvocableResult,
    InvokeOptions,
    Invoker,
    UriPackageOrWrapper,
    WrapAbortError,
    WrapError,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_encode
from wasmtime import Instance, Store

from .exports import WrapExports
from .instance import create_instance
from .types.state import State


class WasmWrapper(Wrapper[UriPackageOrWrapper]):
    """WasmWrapper implements the Wrapper interface for Wasm wrappers.

    Attributes:
        file_reader: The file reader used to read the wrapper files.
        wasm_module: The Wasm module file of the wrapper.
        manifest: The manifest of the wrapper.
    """

    file_reader: FileReader
    wasm_module: bytes
    manifest: AnyWrapManifest

    def __init__(
        self, file_reader: FileReader, wasm_module: bytes, manifest: AnyWrapManifest
    ):
        """Initialize a new WasmWrapper instance."""
        self.file_reader = file_reader
        self.wasm_module = wasm_module
        self.manifest = manifest

    def get_manifest(self) -> AnyWrapManifest:
        """Get the manifest of the wrapper."""
        return self.manifest

    def get_wasm_module(self) -> bytes:
        """Get the Wasm module of the wrapper."""
        return self.wasm_module

    async def get_file(self, options: GetFileOptions) -> Union[str, bytes]:
        """Get a file from the wrapper.

        Args:
            options: The options to use when getting the file.

        Returns:
            The file contents as string or bytes according to encoding or an error.
        """
        data = await self.file_reader.read_file(options.path)
        return data.decode(encoding=options.encoding) if options.encoding else data

    def create_wasm_instance(
        self,
        store: Store,
        state: State,
        invoker: Invoker[UriPackageOrWrapper],
        options: InvokeOptions[UriPackageOrWrapper],
    ) -> Instance:
        """Create a new Wasm instance for the wrapper.

        Args:
            store: The Wasm store to use when creating the instance.
            state: The Wasm wrapper state to use when creating the instance.
            invoker: The invoker to use when creating the instance.

        Returns:
            The Wasm instance of the wrapper Wasm module.
        """
        try:
            return create_instance(store, self.wasm_module, state, invoker)
        except Exception as err:
            raise WrapAbortError(
                options, "Unable to instantiate the wasm module"
            ) from err

    async def invoke(
        self,
        options: InvokeOptions[UriPackageOrWrapper],
        invoker: Invoker[UriPackageOrWrapper],
    ) -> InvocableResult:
        """Invoke the wrapper.

        Args:
            options: The options to use when invoking the wrapper.
            invoker: The invoker to use when invoking the wrapper.

        Returns:
            The result of the invocation or an error.
        """
        if not (options.uri and options.method):
            raise WrapError(
                dedent(
                    f"""
                    Expected invocation uri and method to be defiened got:
                    uri: {options.uri}
                    method: {options.method}
                    """
                )
            )

        state = State(invoke_options=options)

        encoded_args = (
            state.invoke_options.args
            if isinstance(state.invoke_options.args, bytes)
            else msgpack_encode(state.invoke_options.args)
        )
        encoded_env = msgpack_encode(state.invoke_options.env)

        method_length = len(state.invoke_options.method)
        args_length = len(encoded_args)
        env_length = len(encoded_env)

        store = Store()
        instance = self.create_wasm_instance(store, state, invoker, options)

        exports = WrapExports(instance, store)
        result = exports.__wrap_invoke__(method_length, args_length, env_length)

        if result and state.invoke_result and state.invoke_result.result:
            # Note: currently we only return not None result from Wasm module
            return InvocableResult(result=state.invoke_result.result, encoded=True)
        raise WrapAbortError(
            options,
            "Expected a result from the Wasm module",
        )
