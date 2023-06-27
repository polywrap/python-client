"""This module contains abort family of imports for the Wasm module."""
from polywrap_core import WrapAbortError

from .types import BaseWrapImports


class WrapAbortImports(BaseWrapImports):
    """Defines the abort family of imports for the Wasm module."""

    def wrap_abort(
        self,
        msg_ptr: int,
        msg_len: int,
        file_ptr: int,
        file_len: int,
        line: int,
        column: int,
    ) -> None:
        """Abort the Wasm module and raise an exception.

        Args:
            msg_ptr (int): The pointer to the message string in memory.
            msg_len (int): The length of the message string in memory.
            file_ptr (int): The pointer to the filename string in memory.
            file_len (int): The length of the filename string in memory.
            line (int): The line of the file at where the abort occured.
            column (int): The column of the file at where the abort occured.

        Raises:
            WasmAbortError: since the Wasm module aborted during invocation.
        """
        msg = self.read_string(
            msg_ptr,
            msg_len,
        )
        file = self.read_string(
            file_ptr,
            file_len,
        )

        if self.state.subinvoke_result and self.state.subinvoke_result.error:
            # If the error thrown by Wasm module is the same as the subinvoke error,
            #  then we can notify the subinvoke error was cause of the Wasm module abort.
            raise WrapAbortError(
                self.state.invoke_options,
                f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]",
            ) from self.state.subinvoke_result.error

        raise WrapAbortError(
            self.state.invoke_options,
            f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]",
        )
