"""This module contains the debug family of imports for the Wasm module."""
from .types import BaseWrapImports


class WrapDebugImports(BaseWrapImports):
    """Defines the debug family of imports for the Wasm module."""

    def wrap_debug_log(self, msg_ptr: int, msg_len: int) -> None:
        """Print the transmitted message from the Wasm module to host stdout.

        Args:
            msg_ptr (int): The pointer to the message string in memory.
            msg_len (int): The length of the message string in memory.
        """
        msg = self.read_string(msg_ptr, msg_len)
        print(msg)
