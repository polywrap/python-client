"""This module contains the imports of the Wasm wrapper module."""
from typing import Any, List, cast

from polywrap_core import Invoker, InvokerOptions, Uri
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_result import Err, Ok, Result
from unsync import Unfuture, unsync
from wasmtime import (
    FuncType,
    Memory,
    Store,
    ValType,
)

from .buffer import read_bytes, read_string, write_bytes, write_string
from .errors import WasmAbortError
from .types.state import State


@unsync
async def unsync_invoke(invoker: Invoker, options: InvokerOptions) -> Result[Any]:
    """Utility function to perform an unsync invoke call."""
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

    def wrap_debug_log(self, ptr: int, len: int) -> None:
        """Print the transmitted message from the Wasm module to stdout.

        Args:
            ptr: The pointer to the string in memory.
            len: The length of the string in memory.
        """
        msg = read_string(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), ptr, len
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
            msgpack_decode(self.state.args) if self.state.args else None,
            msgpack_decode(self.state.env) if self.state.env else None,
            f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]",
        )

    def wrap_load_env(self, ptr: int) -> None:
        """Load the environment variables into the Wasm module.

        Args:
            ptr: The pointer to the environment variables in memory.

        Raises:
            WasmAbortError: if the environment variables are not set from the host.
        """
        if not self.state.env:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args) if self.state.args else None,
                msgpack_decode(self.state.env) if self.state.env else None,
                "__wrap_load_env: Environment variables are not set from the host.",
            )
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.env,
            ptr,
        )

    def wrap_invoke_args(self, method_ptr: int, args_ptr: int) -> None:
        """Send the method and args of the function to be invoked to the Wasm module.

        Args:
            method_ptr: The pointer to the method name string in memory.
            args_ptr: The pointer to the method args bytes in memory.

        Raises:
            WasmAbortError: if the method or args are not set from the host.
        """

        if not self.state.method:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args) if self.state.args else None,
                msgpack_decode(self.state.env) if self.state.env else None,
                "__wrap_invoke_args: method is not set from the host."
            )

        if not self.state.args:
            raise WasmAbortError(
                self.state.uri,
                self.state.method,
                msgpack_decode(self.state.args) if self.state.args else None,
                msgpack_decode(self.state.env) if self.state.env else None,
                "__wrap_invoke_args: args is not set from the host."
            )

        write_string(self.memory.data_ptr(self.store), self.memory.data_len(self.store), self.state.method, method_ptr)

        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            bytearray(self.state.args),
            args_ptr,
        )

    def wrap_invoke_result(self, offset: int, length: int) -> None:
        """Send the result of the invoked function to the host from the Wasm module.

        Args:
            offset: The offset of the result bytes in memory.
            length: The length of the result bytes in memory.
        """
        result = read_bytes(self.memory.data_ptr(self.store), self.memory.data_len(self.store), offset, length)
        self.state.invoke["result"] = result

    def wrap_invoke_error(self, offset: int, length: int):
        """Send the error of the invoked function to the host from the Wasm module.

        Args:
            offset: The offset of the error string in memory.
            length: The length of the error string in memory.
        """
        error = read_string(self.memory.data_ptr(self.store), self.memory.data_len(self.store), offset, length)
        self.state.invoke["error"] = error

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
        self.state.subinvoke["result"] = None
        self.state.subinvoke["error"] = None

        uri = read_string(self.memory.data_ptr(self.store), self.memory.data_len(self.store), uri_ptr, uri_len)
        method = read_string(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), method_ptr, method_len
        )
        args = read_bytes(self.memory.data_ptr(self.store), self.memory.data_len(self.store), args_ptr, args_len)

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            self.invoker,
            InvokerOptions(uri=Uri(uri), method=method, args=args, encode_result=True),
        )
        result = unfuture_result.result()

        if result.is_ok():
            if isinstance(result.unwrap(), (bytes, bytearray)):
                self.state.subinvoke["result"] = result.unwrap()
                return True
            self.state.subinvoke["result"] = msgpack_encode(result.unwrap())
            return True
        elif result.is_err():
            error = cast(Err, result).unwrap_err()
            self.state.subinvoke["error"] = "".join(str(x) for x in error.args)
            return False
        else:
            raise RuntimeError("subinvocation failed!")

    def wrap_subinvoke_result_len(self) -> int:
        """Get the length of the result bytes of the subinvocation.
        
        Returns:
            The length of the result bytes of the subinvocation.
        """
        if not self.state.subinvoke["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_result_len: subinvoke.result is not set"
            )
        return len(self.state.subinvoke["result"])

    wrap_subinvoke_result_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_result(ptr: int) -> None:
        if not self.state.subinvoke["result"]:
            raise WasmAbortError("__wrap_subinvoke_result: subinvoke.result is not set")
        write_bytes(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), self.state.subinvoke["result"], ptr
        )

    wrap_subinvoke_error_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_error_len() -> int:
        if not self.state.subinvoke["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_error_len: subinvoke.error is not set"
            )
        return len(self.state.subinvoke["error"])

    wrap_subinvoke_error_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_error(ptr: int) -> None:
        if not self.state.subinvoke["error"]:
            raise WasmAbortError("__wrap_subinvoke_error: subinvoke.error is not set")
        write_string(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), self.state.subinvoke["error"], ptr
        )

    wrap_subinvoke_implementation_type = FuncType(
        [
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
        ],
        [ValType.i32()],
    )

    def wrap_subinvoke_implementation(
        interface_uri_ptr: int,
        interface_uri_len: int,
        impl_uri_ptr: int,
        impl_uri_len: int,
        method_ptr: int,
        method_len: int,
        args_ptr: int,
        args_len: int,
    ) -> bool:
        self.state.subinvoke_implementation["result"] = None
        self.state.subinvoke_implementation["error"] = None

        interface_uri = read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            interface_uri_ptr,
            interface_uri_len,
        )
        impl_uri = read_string(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), impl_uri_ptr, impl_uri_len
        )
        method = read_string(
            self.memory.data_ptr(self.store), self.memory.data_len(self.store), method_ptr, method_len
        )
        args = read_bytes(self.memory.data_ptr(self.store), self.memory.data_len(self.store), args_ptr, args_len)

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            invoker,
            InvokerOptions(
                uri=Uri(impl_uri), method=method, args=args, encode_result=True
            ),
        )
        result = unfuture_result.result()

        if result.is_ok():
            result = cast(Ok[bytes], result)
            self.state.subinvoke_implementation["result"] = result.unwrap()
            return True
        elif result.is_err():
            error = cast(Err, result).unwrap_err()
            self.state.subinvoke_implementation["error"] = "".join(
                str(x) for x in error.args
            )
            return False
        else:
            raise WasmAbortError(
                f"interface implementation subinvoke failed for uri: {interface_uri}!"
            )

    wrap_subinvoke_implementation_result_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_implementation_result_len() -> int:
        if not self.state.subinvoke_implementation["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_result_len: subinvoke_implementation.result is not set"
            )
        return len(self.state.subinvoke_implementation["result"])

    wrap_subinvoke_implementation_result_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_implementation_result(ptr: int) -> None:
        if not self.state.subinvoke_implementation["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_result: subinvoke_implementation.result is not set"
            )
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.subinvoke_implementation["result"],
            ptr,
        )

    wrap_subinvoke_implementation_error_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_implementation_error_len() -> int:
        if not self.state.subinvoke_implementation["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_error_len: subinvoke_implementation.error is not set"
            )
        return len(self.state.subinvoke_implementation["error"])

    wrap_subinvoke_implementation_error_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_implementation_error(ptr: int) -> None:
        if not self.state.subinvoke_implementation["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_error: subinvoke_implementation.error is not set"
            )
        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.subinvoke_implementation["error"],
            ptr,
        )

    wrap_get_implementations_type = FuncType(
        [ValType.i32(), ValType.i32()], [ValType.i32()]
    )

    def wrap_get_implementations(uri_ptr: int, uri_len: int) -> bool:
        uri = read_string(self.memory.data_ptr(self.store), self.memory.data_len(self.store), uri_ptr, uri_len)
        result = invoker.get_implementations(uri=Uri(uri))
        if result.is_err():
            raise WasmAbortError(
                f"failed calling invoker.get_implementations({repr(Uri(uri))})"
            ) from result.unwrap_err()
        maybeImpls = result.unwrap()
        implementations: List[str] = (
            [uri.uri for uri in maybeImpls] if maybeImpls else []
        )
        self.state.get_implementations_result = msgpack_encode(implementations)
        return len(implementations) > 0

    wrap_get_implementations_result_len_type = FuncType([], [ValType.i32()])

    def wrap_get_implementations_result_len() -> int:
        if not self.state.get_implementations_result:
            raise WasmAbortError(
                "__wrap_get_implementations_result_len: get_implementations_result is not set"
            )
        return len(self.state.get_implementations_result)

    wrap_get_implementations_result_type = FuncType([ValType.i32()], [])

    def wrap_get_implementations_result(ptr: int) -> None:
        if not self.state.get_implementations_result:
            raise WasmAbortError(
                "__wrap_get_implementations_result: get_implementations_result is not set"
            )
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            self.state.get_implementations_result,
            ptr,
        )