from typing import List
from polywrap_core import Uri, WrapAbortError
from polywrap_msgpack import msgpack_encode

from .types import BaseWrapImports


class WrapGetImplementationsImports(BaseWrapImports):
    def wrap_get_implementations(self, uri_ptr: int, uri_len: int) -> bool:
        """Get the list of implementations URIs of the given interface URI\
            from the invoker and store it in the state.

        Args:
            uri_ptr: The pointer to the interface URI bytes in memory.
            uri_len: The length of the interface URI bytes in memory.
        """
        uri = Uri.from_str(
            self.read_string(
                uri_ptr,
                uri_len,
            )
        )
        try:
            maybe_implementations = self.invoker.get_implementations(uri=uri)
            implementations: List[str] = (
                [uri.uri for uri in maybe_implementations]
                if maybe_implementations
                else []
            )
            self.state.get_implementations_result = msgpack_encode(implementations)
            return len(implementations) > 0
        except Exception as err:
            raise WrapAbortError(
                self.state.invoke_options,
                f"failed calling invoker.get_implementations({repr(uri)})",
            ) from err

    def wrap_get_implementations_result_len(self) -> int:
        """Get the length of the encoded list of implementations URIs bytes."""
        result = self._get_get_implementations_result(
            "__wrap_get_implementations_result_len"
        )
        return len(result)

    def wrap_get_implementations_result(self, ptr: int) -> None:
        """Write the encoded list of implementations URIs bytes to shared memory\
            at pointer to the Wasm allocated empty list of implementations slot.
        
        Args:
            ptr: The pointer to the empty list of implementations slot in memory.
        """
        result = self._get_get_implementations_result(
            "__wrap_get_implementations_result"
        )
        self.write_bytes(
            ptr,
            result
        )

    def _get_get_implementations_result(self, export_name: str):
        if not self.state.get_implementations_result:
            raise WrapAbortError(
                self.state.invoke_options,
                f"{export_name}: get_implementations_result is not set",
            )
        return self.state.get_implementations_result
