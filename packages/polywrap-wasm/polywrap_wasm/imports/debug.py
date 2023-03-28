from .types import BaseWrapImports


class WrapDebugImports(BaseWrapImports):
    def wrap_debug_log(self, msg_ptr: int, msg_len: int) -> None:
        """Print the transmitted message from the Wasm module to host stdout.

        Args:
            ptr: The pointer to the message string in memory.
            len: The length of the message string in memory.
        """
        msg = self.read_string(msg_ptr, msg_len)
        print(msg)