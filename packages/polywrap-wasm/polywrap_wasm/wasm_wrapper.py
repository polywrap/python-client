"""This module contains the WasmWrapper class for invoking Wasm wrappers."""
# pylint: disable=too-many-locals
from textwrap import dedent
from typing import Any, Dict, Optional, Union

from polywrap_core import (
    FileReader,
    InvocableResult,
    Invoker,
    Uri,
    UriResolutionContext,
    WrapAbortError,
    WrapError,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_encode
from wasmtime import Instance, Store

from .exports import WrapExports
from .instance import create_instance
from .types.state import InvokeOptions, State


class WasmWrapper(Wrapper):
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

    def get_file(
        self, path: str, encoding: Optional[str] = "utf-8"
    ) -> Union[str, bytes]:
        """Get a file from the wrapper.

        Args:
            options: The options to use when getting the file.

        Returns:
            The file contents as string or bytes according to encoding or an error.
        """
        data = self.file_reader.read_file(path)
        return data.decode(encoding=encoding) if encoding else data

    def create_wasm_instance(
        self, store: Store, state: State, client: Optional[Invoker]
    ) -> Instance:
        """Create a new Wasm instance for the wrapper.

        Args:
            store: The Wasm store to use when creating the instance.
            state: The Wasm wrapper state to use when creating the instance.
            client: The client to use when creating the instance.

        Returns:
            The Wasm instance of the wrapper Wasm module.
        """
        try:
            return create_instance(store, self.wasm_module, state, client)
        except Exception as err:
            raise WrapAbortError(
                state.invoke_options, "Unable to instantiate the wasm module"
            ) from err

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Dict[str, Any]] = None,
        env: Optional[Dict[str, Any]] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        client: Optional[Invoker] = None,
    ) -> InvocableResult:
        """Invoke the wrapper.

        Args:
            options: The options to use when invoking the wrapper.
            client: The client to use when invoking the wrapper.

        Returns:
            The result of the invocation or an error.
        """
        if not (uri and method):
            raise WrapError(
                dedent(
                    f"""
                    Expected invocation uri and method to be defiened got:
                    uri: {uri}
                    method: {method}
                    """
                )
            )

        state = State(
            invoke_options=InvokeOptions(
                uri=uri,
                method=method,
                args=args,
                env=env,
                resolution_context=resolution_context,
            )
        )

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
        instance = self.create_wasm_instance(store, state, client)

        exports = WrapExports(instance, store)
        result = exports.__wrap_invoke__(method_length, args_length, env_length)

        if result and state.invoke_result and state.invoke_result.result:
            # Note: currently we only return not None result from Wasm module
            return InvocableResult(result=state.invoke_result.result, encoded=True)
        raise WrapAbortError(
            state.invoke_options,
            "Expected a result from the Wasm module",
        )


__all__ = ["WasmWrapper"]
