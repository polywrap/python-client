from polywrap_core import WrapAbortError

from .types import BaseWrapImports


class WrapAbortImports(BaseWrapImports):
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
            msg_ptr: The pointer to the message string in memory.
            msg_len: The length of the message string in memory.
            file_ptr: The pointer to the filename string in memory.
            file_len: The length of the filename string in memory.
            line: The line of the file at where the abort occured.
            column: The column of the file at where the abort occured.

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
        raise WrapAbortError(
            self.state.invoke_options,
            f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]",
        )
