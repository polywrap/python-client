"""This module contains the subinvoke imports for the Wasm module."""
from polywrap_core import Uri, WrapAbortError
from polywrap_msgpack import msgpack_encode

from ..types import InvokeResult
from .types import BaseWrapImports


class WrapSubinvokeImports(BaseWrapImports):
    """Defines the subinvoke family of imports for the Wasm module."""

    def wrap_subinvoke(
        self,
        uri_ptr: int,
        uri_len: int,
        method_ptr: int,
        method_len: int,
        args_ptr: int,
        args_len: int,
    ) -> bool:
        """Subinvoke a function of any wrapper from the Wasm module.

        Args:
            uri_ptr (int): The pointer to the uri string in memory.
            uri_len (int): The length of the uri string in memory.
            method_ptr (int): The pointer to the method string in memory.
            method_len (int): The length of the method string in memory.
            args_ptr (int): The pointer to the args bytes in memory.
            args_len (int): The length of the args bytes in memory.

        Returns:
            True if the subinvocation was successful, False otherwise.
        """
        self.state.subinvoke_result = None

        uri = self._get_subinvoke_uri(uri_ptr, uri_len)
        method = self._get_subinvoke_method(method_ptr, method_len)
        args = self._get_subinvoke_args(args_ptr, args_len)

        if not self.invoker:
            raise WrapAbortError(
                invoke_options=self.state.invoke_options,
                message="Expected invoker to be defined got None",
            )

        try:
            result = self.invoker.invoke(
                uri=uri,
                method=method,
                args=args,
                encode_result=True,
            )
            if isinstance(result, bytes):
                self.state.subinvoke_result = InvokeResult(result=result)
                return True
            self.state.subinvoke_result = InvokeResult(result=msgpack_encode(result))
            return True
        except Exception as err:
            self.state.subinvoke_result = InvokeResult(error=err)
            return False

    def wrap_subinvoke_result_len(self) -> int:
        """Get the length of the subinvocation result bytes."""
        result = self._get_subinvoke_result("__wrap_subinvoke_result_len")
        return len(result)

    def wrap_subinvoke_result(self, ptr: int) -> None:
        """Write the result of the subinvocation to shared memory.

        Args:
            ptr (int): The pointer to the empty result bytes slot in memory.
        """
        result = self._get_subinvoke_result("__wrap_subinvoke_result")
        self.write_bytes(ptr, result)

    def wrap_subinvoke_error_len(self) -> int:
        """Get the length of the subinocation error message in case of an error."""
        error = self._get_subinvoke_error("__wrap_subinvoke_error_len")
        error_message = repr(error)
        return len(error_message)

    def wrap_subinvoke_error(self, ptr: int) -> None:
        """Write the subinvocation error message to shared memory\
            at pointer to the Wasm allocated empty error message slot.

        Args:
            ptr (int): The pointer to the empty error message slot in memory.
        """
        error = self._get_subinvoke_error("__wrap_subinvoke_error")
        error_message = repr(error)
        self.write_string(ptr, error_message)

    def _get_subinvoke_uri(self, uri_ptr: int, uri_len: int) -> Uri:
        uri = self.read_string(
            uri_ptr,
            uri_len,
        )
        return Uri.from_str(uri)

    def _get_subinvoke_method(self, method_ptr: int, method_len: int) -> str:
        return self.read_string(
            method_ptr,
            method_len,
        )

    def _get_subinvoke_args(self, args_ptr: int, args_len: int) -> bytes:
        return self.read_bytes(
            args_ptr,
            args_len,
        )

    def _get_subinvoke_result(self, export_name: str) -> bytes:
        if not self.state.subinvoke_result:
            raise WrapAbortError(
                self.state.invoke_options, f"{export_name}: subinvoke.result is not set"
            )
        if self.state.subinvoke_result.error:
            raise WrapAbortError(
                self.state.invoke_options,
                f"{export_name}: subinvocation failed",
            ) from self.state.subinvoke_result.error
        if not self.state.subinvoke_result.result:
            raise WrapAbortError(
                self.state.invoke_options,
                f"{export_name}: subinvoke_result.result is not set",
            )
        return self.state.subinvoke_result.result

    def _get_subinvoke_error(self, export_name: str) -> Exception:
        if not self.state.subinvoke_result:
            raise WrapAbortError(
                self.state.invoke_options, f"{export_name}: subinvoke_result is not set"
            )
        if not self.state.subinvoke_result.error:
            raise WrapAbortError(
                self.state.invoke_options,
                f"{export_name}: subinvoke_result.error is not set",
            )
        return self.state.subinvoke_result.error
