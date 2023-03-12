"""This module contains the imports of the Wasm wrapper module."""
import traceback
from typing import Any, List

from polywrap_core import Invoker, InvokerOptions, Uri
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_result import Err, Ok, Result
from unsync import Unfuture, unsync
from wasmtime import Memory, Store

from .buffer import read_bytes, read_string, write_bytes, write_string
from .errors import WasmAbortError
from .types.state import State


@unsync
async def unsync_invoke(invoker: Invoker, options: InvokerOptions) -> Result[Any]:
    """Perform an unsync invoke call."""
    return await invoker.invoke(options)


class WrapImports:
    """WrapImports is a class that contains the imports of the Wasm wrapper module."""

    def __init__(
        self, memory: Memory, store: Store, state: State, invoker: Invoker
    ) -> None:
        """Initialize the WrapImports instance.

        Args:
            memory: The Wasm memory instance.
            store: The Wasm store instance.
            state: The state of the Wasm module.
            invoker: The invoker instance.
        """
        self.memory = memory
        self.store = store
        self.state = state
        self.invoker = invoker

    def wrap_debug_log(self, msg_ptr: int, msg_len: int) -> None:
        """Print the transmitted message from the Wasm module to host stdout.

        Args:
            ptr: The pointer to the message string in memory.
            len: The length of the message string in memory.
        """
        msg = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            msg_ptr,
            msg_len,
        )
        print(msg)

    def wrap_abort(
        self,
        msg_offset: int,
        msg_len: int,
        file_offset: int,
        file_len: int,
        line: int,
        column: int,
    ) -> None:
        """Abort the Wasm module and raise an exception.

        Args:
            msg_offset: The offset of the message string in memory.
            msg_len: The length of the message string in memory.
            file_offset: The offset of the filename string in memory.
            file_len: The length of the filename string in memory.
            line: The line of the file at where the abort occured.
            column: The column of the file at where the abort occured.

        Raises:
            WasmAbortError: since the Wasm module aborted during invocation.
        """
        msg = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            msg_offset,
            msg_len,
        )
        file = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            file_offset,
            file_len,
        )
        raise WasmAbortError(
            self.state.uri,
            self.state.method,
            msgpack_decode(self.state.args).unwrap() if self.state.args else None,
            msgpack_decode(self.state.env).unwrap() if self.state.env else None,
            f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]",
        )

    def wrap_load_env(self, ptr: int) -> None:
        """Write the env in the shared memory at Wasm allocated empty env slot.

        Args:
            ptr: The pointer to the empty env slot in memory.

        Raises:
            WasmAbortError: if the env is not set from the host.
        """
        if not self.state.env:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_load_env: Environment variables are not set from the host.",
            )
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.env,
            ptr,
        )

    def wrap_invoke_args(self, method_ptr: int, args_ptr: int) -> None:
        """Write the method and args of the function to be invoked in the shared memory\
            at Wasm allocated empty method and args slots.

        Args:
            method_ptr: The pointer to the empty method name string slot in memory.
            args_ptr: The pointer to the empty method args bytes slot in memory.

        Raises:
            WasmAbortError: if the method or args are not set from the host.
        """
        if not self.state.method:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_invoke_args: method is not set from the host.",
            )

        if not self.state.args:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_invoke_args: args is not set from the host.",
            )

        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.method,
            method_ptr,
        )

        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            bytearray(self.state.args),
            args_ptr,
        )

    def wrap_invoke_result(self, offset: int, length: int) -> None:
        """Read and store the result of the invoked Wasm function written\
            in the shared memory by the Wasm module in the state.

        Args:
            offset: The offset of the result bytes in memory.
            length: The length of the result bytes in memory.
        """
        result = read_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            offset,
            length,
        )
        self.state.invoke_result = Ok(result)

    def wrap_invoke_error(self, offset: int, length: int):
        """Read and store the error of the invoked Wasm function written\
            in the shared memory by the Wasm module in the state.

        Args:
            offset: The offset of the error string in memory.
            length: The length of the error string in memory.
        """
        error = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            offset,
            length,
        )
        self.state.invoke_result = Err.with_tb(
            WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                f"__wrap_invoke_error: {error}",
            )
        )

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
            uri_ptr: The pointer to the uri string in memory.
            uri_len: The length of the uri string in memory.
            method_ptr: The pointer to the method string in memory.
            method_len: The length of the method string in memory.
            args_ptr: The pointer to the args bytes in memory.
            args_len: The length of the args bytes in memory.

        Returns:
            True if the subinvocation was successful, False otherwise.
        """
        self.state.subinvoke_result = None

        uri = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            uri_ptr,
            uri_len,
        )
        method = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            method_ptr,
            method_len,
        )
        args = read_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            args_ptr,
            args_len,
        )

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            self.invoker,
            InvokerOptions(uri=Uri(uri), method=method, args=args, encode_result=True),
        )
        result = unfuture_result.result()

        if result.is_ok():
            if isinstance(result.unwrap(), (bytes, bytearray)):
                self.state.subinvoke_result = result
                return True
            self.state.subinvoke_result = msgpack_encode(result.unwrap())
            return True

        self.state.subinvoke_result = result
        return False

    def wrap_subinvoke_result_len(self) -> int:
        """Get the length of the subinvocation result bytes."""
        if not self.state.subinvoke_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_result_len: subinvoke_result is not set",
            )
        if self.state.subinvoke_result.is_err():
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_result_len: subinvocation failed",
            ) from self.state.subinvoke_result.unwrap_err()
        return len(self.state.subinvoke_result.unwrap())

    def wrap_subinvoke_result(self, ptr: int) -> None:
        """Write the result of the subinvocation to shared memory.

        Args:
            ptr: The pointer to the empty result bytes slot in memory.
        """
        if not self.state.subinvoke_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_result: subinvoke.result is not set",
            )
        if self.state.subinvoke_result.is_err():
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_result_len: subinvocation failed",
            ) from self.state.subinvoke_result.unwrap_err()
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.subinvoke_result.unwrap(),
            ptr,
        )

    def wrap_subinvoke_error_len(self) -> int:
        """Get the length of the subinocation error message in case of an error."""
        if not self.state.subinvoke_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_error_len: subinvoke.error is not set",
            )
        error = self.state.subinvoke_result.unwrap_err()
        error_message = "".join(
            traceback.format_exception(error.__class__, error, error.__traceback__)
        )
        return len(error_message)

    def wrap_subinvoke_error(self, ptr: int) -> None:
        """Write the subinvocation error message to shared memory\
            at pointer to the Wasm allocated empty error message slot.

        Args:
            ptr: The pointer to the empty error message slot in memory.
        """
        if not self.state.subinvoke_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_error: subinvoke.error is not set",
            )
        error = self.state.subinvoke_result.unwrap_err()
        error_message = "".join(
            traceback.format_exception(error.__class__, error, error.__traceback__)
        )
        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            error_message,
            ptr,
        )

    def wrap_subinvoke_implementation(
        self,
        interface_uri_ptr: int,
        interface_uri_len: int,
        impl_uri_ptr: int,
        impl_uri_len: int,
        method_ptr: int,
        method_len: int,
        args_ptr: int,
        args_len: int,
    ) -> bool:
        """Subinvoke an implementation.

        Args:
            interface_uri_ptr: The pointer to the interface URI in shared memory.
            interface_uri_len: The length of the interface URI in shared memory.
            impl_uri_ptr: The pointer to the implementation URI in shared memory.
            impl_uri_len: The length of the implementation URI in shared memory.
            method_ptr: The pointer to the method name in shared memory.
            method_len: The length of the method name in shared memory.
            args_ptr: The pointer to the arguments buffer in shared memory.
            args_len: The length of the arguments buffer in shared memory.
        """
        self.state.subinvoke_implementation_result = None

        _interface_uri = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            interface_uri_ptr,
            interface_uri_len,
        )
        impl_uri = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            impl_uri_ptr,
            impl_uri_len,
        )
        method = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            method_ptr,
            method_len,
        )
        args = read_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            args_ptr,
            args_len,
        )

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            self.invoker,
            InvokerOptions(
                uri=Uri(impl_uri), method=method, args=args, encode_result=True
            ),
        )
        result = unfuture_result.result()

        if result.is_ok():
            if isinstance(result.unwrap(), (bytes, bytearray)):
                self.state.subinvoke_implementation_result = result
                return True
            self.state.subinvoke_implementation_result = msgpack_encode(result.unwrap())
            return True

        self.state.subinvoke_implementation_result = result
        return False

    def wrap_subinvoke_implementation_result_len(self) -> int:
        """Get the length of the subinvocation implementation result bytes."""
        if not self.state.subinvoke_implementation_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_implementation_result_len: \
                    subinvoke_implementation_result is not set",
            )
        if self.state.subinvoke_implementation_result.is_err():
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_implementation_result_len: subinvocation failed",
            ) from self.state.subinvoke_implementation_result.unwrap_err()
        return len(self.state.subinvoke_implementation_result.unwrap())

    def wrap_subinvoke_implementation_result(self, ptr: int) -> None:
        """Write the result of the implementation subinvocation to shared memory.

        Args:
            ptr: The pointer to the empty result bytes slot in memory.
        """
        if not self.state.subinvoke_implementation_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_implementation_result: \
                    subinvoke_implementation_result is not set",
            )
        if self.state.subinvoke_implementation_result.is_err():
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_implementation_result: subinvocation failed",
            ) from self.state.subinvoke_implementation_result.unwrap_err()
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.subinvoke_implementation_result.unwrap(),
            ptr,
        )

    def wrap_subinvoke_implementation_error_len(self) -> int:
        """Get the length of the implementation subinocation error message in case of an error."""
        if not self.state.subinvoke_implementation_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_implementation_error_len: \
                    subinvoke_implementation_result is not set",
            )
        error = self.state.subinvoke_implementation_result.unwrap_err()
        error_message = "".join(
            traceback.format_exception(error.__class__, error, error.__traceback__)
        )
        return len(error_message)

    def wrap_subinvoke_implementation_error(self, ptr: int) -> None:
        """Write the subinvocation error message to shared memory\
            at pointer to the Wasm allocated empty error message slot.

        Args:
            ptr: The pointer to the empty error message slot in memory.
        """
        if not self.state.subinvoke_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_subinvoke_error: subinvoke.error is not set",
            )
        error = self.state.subinvoke_result.unwrap_err()
        error_message = "".join(
            traceback.format_exception(error.__class__, error, error.__traceback__)
        )
        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            error_message,
            ptr,
        )

    def wrap_get_implementations(self, uri_ptr: int, uri_len: int) -> bool:
        """Get the list of implementations URIs of the given interface URI\
            from the invoker and store it in the state.
        
        Args:
            uri_ptr: The pointer to the interface URI bytes in memory.
            uri_len: The length of the interface URI bytes in memory.
        """
        uri = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            uri_ptr,
            uri_len,
        )
        result = self.invoker.get_implementations(uri=Uri(uri))
        if result.is_err():
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                f"failed calling invoker.get_implementations({repr(Uri(uri))})",
            ) from result.unwrap_err()
        maybe_implementations = result.unwrap()
        implementations: List[str] = (
            [uri.uri for uri in maybe_implementations] if maybe_implementations else []
        )
        self.state.get_implementations_result = msgpack_encode(implementations).unwrap()
        return len(implementations) > 0

    def wrap_get_implementations_result_len(self) -> int:
        """Get the length of the encoded list of implementations URIs bytes."""
        if not self.state.get_implementations_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_get_implementations_result_len: get_implementations_result is not set",
            )
        return len(self.state.get_implementations_result)

    def wrap_get_implementations_result(self, ptr: int) -> None:
        """Write the encoded list of implementations URIs bytes to shared memory\
            at pointer to the Wasm allocated empty list of implementations slot.
        
        Args:
            ptr: The pointer to the empty list of implementations slot in memory.
        """
        if not self.state.get_implementations_result:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args).unwrap() if self.state.args else None,
                msgpack_decode(self.state.env).unwrap() if self.state.env else None,
                "__wrap_get_implementations_result: get_implementations_result is not set",
            )
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.get_implementations_result,
            ptr,
        )
