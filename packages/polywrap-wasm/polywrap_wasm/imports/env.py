"""This module contains the env family of imports for the Wasm module."""
from polywrap_core import WrapAbortError
from polywrap_msgpack import msgpack_encode

from .types import BaseWrapImports


class WrapEnvImports(BaseWrapImports):
    """Defines the env family of imports for the Wasm module."""

    def wrap_load_env(self, ptr: int) -> None:
        """Write the env in the shared memory at Wasm allocated empty env slot.

        Args:
            ptr (int): The pointer to the empty env slot in memory.

        Raises:
            WasmAbortError: if the env is not set from the host.
        """
        if not self.state.invoke_options.env:
            raise WrapAbortError(
                self.state.invoke_options,
                "__wrap_load_env: Environment variables are not set from the host.",
            )
        self.write_bytes(
            ptr,
            msgpack_encode(self.state.invoke_options.env),
        )
