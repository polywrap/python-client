"""This module contains the imports for the invoke family of functions."""
from polywrap_core import WrapAbortError
from polywrap_msgpack import msgpack_encode

from ..types import InvokeResult
from .types import BaseWrapImports


class WrapInvokeImports(BaseWrapImports):
    """Defines the invoke family of imports for the Wasm module."""

    def wrap_invoke_args(self, method_ptr: int, args_ptr: int) -> None:
        """Write the method and args of the function to be invoked in the shared memory\
            at Wasm allocated empty method and args slots.

        Args:
            method_ptr (int): The pointer to the empty method name string slot in memory.
            args_ptr (int): The pointer to the empty method args bytes slot in memory.

        Raises:
            WasmAbortError: if the method or args are not set from the host.
        """
        self.write_string(
            method_ptr,
            self.state.invoke_options.method,
        )

        encoded_args = bytearray(
            self.state.invoke_options.args
            if isinstance(self.state.invoke_options.args, bytes)
            else msgpack_encode(self.state.invoke_options.args)
        )

        self.write_bytes(
            args_ptr,
            encoded_args,
        )

    def wrap_invoke_result(self, ptr: int, length: int) -> None:
        """Read and store the result of the invoked Wasm function written\
            in the shared memory by the Wasm module in the state.

        Args:
            ptr (int): The pointer to the result bytes in memory.
            length (int): The length of the result bytes in memory.
        """
        result = self.read_bytes(
            ptr,
            length,
        )
        self.state.invoke_result = InvokeResult(result=result)

    def wrap_invoke_error(self, ptr: int, length: int):
        """Read and store the error of the invoked Wasm function written\
            in the shared memory by the Wasm module in the state.

        Args:
            ptr (int): The pointer to the error string in memory.
            length (int): The length of the error string in memory.
        """
        error = self.read_string(
            ptr,
            length,
        )

        self.state.invoke_result = InvokeResult(error=error)

        raise WrapAbortError(self.state.invoke_options, f"__wrap_invoke_error: {error}")
