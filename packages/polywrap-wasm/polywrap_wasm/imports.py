from textwrap import dedent
from typing import Any, List, cast

from polywrap_core import Invoker, InvokerOptions, Uri
from polywrap_msgpack import msgpack_encode
from polywrap_result import Err, Ok, Result
from unsync import Unfuture, unsync
from wasmtime import (
    FuncType,
    Instance,
    Limits,
    Linker,
    Memory,
    MemoryType,
    Module,
    Store,
    ValType,
)

from .buffer import read_bytes, read_string, write_bytes, write_string
from .errors import WasmAbortError
from .types.state import State


@unsync
async def unsync_invoke(invoker: Invoker, options: InvokerOptions) -> Result[Any]:
    return await invoker.invoke(options)


def create_memory(
    store: Store,
    module: bytes,
) -> Memory:
    env_memory_import_signature = bytearray(
        [
            # env ; import module name
            0x65,
            0x6E,
            0x76,
            # string length
            0x06,
            # memory ; import field name
            0x6D,
            0x65,
            0x6D,
            0x6F,
            0x72,
            0x79,
            # import kind
            0x02,
            # limits ; https://github.com/sunfishcode/wasm-reference-manual/blob/master/WebAssembly.md#resizable-limits
            # limits ; flags
            # 0x??,
            # limits ; initial
            # 0x__,
        ]
    )
    idx = module.find(env_memory_import_signature)

    if idx < 0:
        raise RuntimeError(
            dedent(
                """
                Unable to find Wasm memory import section. \
                Modules must import memory from the "env" module's\
                "memory" field like so:
                (import "env" "memory" (memory (;0;) #))
                """
            )
        )

    memory_inital_limits = module[idx + len(env_memory_import_signature) + 1]

    return Memory(store, MemoryType(Limits(memory_inital_limits, None)))


def create_instance(
    store: Store,
    module: bytes,
    state: State,
    invoker: Invoker,
) -> Instance:
    linker = Linker(store.engine)

    """
    TODO: Re-check this based on issue https://github.com/polywrap/toolchain/issues/561
    This probably means that memory creation should be moved to its own function 
    """
    mem = create_memory(store, module)

    wrap_debug_log_type = FuncType(
        [ValType.i32(), ValType.i32()],
        [],
    )

    def wrap_debug_log(ptr: int, len: int) -> None:
        msg = read_string(mem.data_ptr(store), mem.data_len(store), ptr, len)
        print(msg)

    wrap_abort_type = FuncType(
        [
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
        ],
        [],
    )

    def wrap_abort(
        msg_offset: int,
        msg_len: int,
        file_offset: int,
        file_len: int,
        line: int,
        column: int,
    ) -> None:
        msg = read_string(mem.data_ptr(store), mem.data_len(store), msg_offset, msg_len)
        file = read_string(
            mem.data_ptr(store), mem.data_len(store), file_offset, file_len
        )
        raise WasmAbortError(
            f"__wrap_abort: {msg}\nFile: {file}\nLocation: [{line},{column}]"
        )

    wrap_load_env_type = FuncType([ValType.i32()], [])

    def wrap_load_env(ptr: int) -> None:
        if not state.env:
            raise WasmAbortError("env: is not set")
        write_bytes(mem.data_ptr(store), mem.data_len(store), state.env, ptr)

    wrap_invoke_args_type = FuncType([ValType.i32(), ValType.i32()], [])

    def wrap_invoke_args(method_ptr: int, args_ptr: int) -> None:
        if not state.method:
            raise WasmAbortError("__wrap_invoke_args: method is not set")
        else:
            write_string(
                mem.data_ptr(store), mem.data_len(store), state.method, method_ptr
            )

        if not state.args:
            raise WasmAbortError("__wrap_invoke_args: args is not set")
        else:
            write_bytes(
                mem.data_ptr(store),
                mem.data_len(store),
                bytearray(state.args),
                args_ptr,
            )

    wrap_invoke_result_type = FuncType([ValType.i32(), ValType.i32()], [])

    def wrap_invoke_result(offset: int, length: int) -> None:
        result = read_bytes(mem.data_ptr(store), mem.data_len(store), offset, length)
        state.invoke["result"] = result

    wrap_invoke_error_type = FuncType([ValType.i32(), ValType.i32()], [])

    def wrap_invoke_error(offset: int, length: int):
        error = read_string(mem.data_ptr(store), mem.data_len(store), offset, length)
        state.invoke["error"] = error

    wrap_subinvoke_type = FuncType(
        [
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
            ValType.i32(),
        ],
        [ValType.i32()],
    )

    def wrap_subinvoke(
        uri_ptr: int,
        uri_len: int,
        method_ptr: int,
        method_len: int,
        args_ptr: int,
        args_len: int,
    ) -> bool:
        state.subinvoke["result"] = None
        state.subinvoke["error"] = None

        uri = read_string(mem.data_ptr(store), mem.data_len(store), uri_ptr, uri_len)
        method = read_string(
            mem.data_ptr(store), mem.data_len(store), method_ptr, method_len
        )
        args = read_bytes(mem.data_ptr(store), mem.data_len(store), args_ptr, args_len)

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            invoker,
            InvokerOptions(uri=Uri(uri), method=method, args=args, encode_result=True),
        )
        result = unfuture_result.result()

        if result.is_ok():
            result = cast(Ok[bytes], result)
            state.subinvoke["result"] = result.unwrap()
            return True
        elif result.is_err():
            error = cast(Err, result).unwrap_err()
            state.subinvoke["error"] = "".join(str(x) for x in error.args)
            return False
        else:
            raise RuntimeError("subinvocation failed!")

    wrap_subinvoke_result_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_result_len() -> int:
        if not state.subinvoke["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_result_len: subinvoke.result is not set"
            )
        return len(state.subinvoke["result"])

    wrap_subinvoke_result_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_result(ptr: int) -> None:
        if not state.subinvoke["result"]:
            raise WasmAbortError("__wrap_subinvoke_result: subinvoke.result is not set")
        write_bytes(
            mem.data_ptr(store), mem.data_len(store), state.subinvoke["result"], ptr
        )

    wrap_subinvoke_error_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_error_len() -> int:
        if not state.subinvoke["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_error_len: subinvoke.error is not set"
            )
        return len(state.subinvoke["error"])

    wrap_subinvoke_error_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_error(ptr: int) -> None:
        if not state.subinvoke["error"]:
            raise WasmAbortError("__wrap_subinvoke_error: subinvoke.error is not set")
        write_string(
            mem.data_ptr(store), mem.data_len(store), state.subinvoke["error"], ptr
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
        state.subinvoke_implementation["result"] = None
        state.subinvoke_implementation["error"] = None

        interface_uri = read_string(
            mem.data_ptr(store),
            mem.data_len(store),
            interface_uri_ptr,
            interface_uri_len,
        )
        impl_uri = read_string(
            mem.data_ptr(store), mem.data_len(store), impl_uri_ptr, impl_uri_len
        )
        method = read_string(
            mem.data_ptr(store), mem.data_len(store), method_ptr, method_len
        )
        args = read_bytes(mem.data_ptr(store), mem.data_len(store), args_ptr, args_len)

        unfuture_result: Unfuture[Result[Any]] = unsync_invoke(
            invoker,
            InvokerOptions(
                uri=Uri(impl_uri), method=method, args=args, encode_result=True
            ),
        )
        result = unfuture_result.result()

        if result.is_ok():
            result = cast(Ok[bytes], result)
            state.subinvoke_implementation["result"] = result.unwrap()
            return True
        elif result.is_err():
            error = cast(Err, result).unwrap_err()
            state.subinvoke_implementation["error"] = "".join(
                str(x) for x in error.args
            )
            return False
        else:
            raise ValueError(
                f"interface implementation subinvoke failed for uri: {interface_uri}!"
            )

    wrap_subinvoke_implementation_result_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_implementation_result_len() -> int:
        if not state.subinvoke_implementation["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_result_len: subinvoke_implementation.result is not set"
            )
        return len(state.subinvoke_implementation["result"])

    wrap_subinvoke_implementation_result_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_implementation_result(ptr: int) -> None:
        if not state.subinvoke_implementation["result"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_result: subinvoke_implementation.result is not set"
            )
        write_bytes(
            mem.data_ptr(store),
            mem.data_len(store),
            state.subinvoke_implementation["result"],
            ptr,
        )

    wrap_subinvoke_implementation_error_len_type = FuncType([], [ValType.i32()])

    def wrap_subinvoke_implementation_error_len() -> int:
        if not state.subinvoke_implementation["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_error_len: subinvoke_implementation.error is not set"
            )
        return len(state.subinvoke_implementation["error"])

    wrap_subinvoke_implementation_error_type = FuncType([ValType.i32()], [])

    def wrap_subinvoke_implementation_error(ptr: int) -> None:
        if not state.subinvoke_implementation["error"]:
            raise WasmAbortError(
                "__wrap_subinvoke_implementation_error: subinvoke_implementation.error is not set"
            )
        write_string(
            mem.data_ptr(store),
            mem.data_len(store),
            state.subinvoke_implementation["error"],
            ptr,
        )

    wrap_get_implementations_type = FuncType(
        [ValType.i32(), ValType.i32()], [ValType.i32()]
    )

    def wrap_get_implementations(uri_ptr: int, uri_len: int) -> bool:
        uri = read_string(mem.data_ptr(store), mem.data_len(store), uri_ptr, uri_len)
        result = invoker.get_implementations(uri=Uri(uri))
        if result.is_err():
            raise WasmAbortError(
                f"failed calling invoker.get_implementations({repr(Uri(uri))})"
            ) from result.unwrap_err()
        maybeImpls = result.unwrap()
        implementations: List[str] = [uri.uri for uri in maybeImpls] if maybeImpls else []
        state.get_implementations_result = msgpack_encode(implementations)
        return len(implementations) > 0

    wrap_get_implementations_result_len_type = FuncType([], [ValType.i32()])

    def wrap_get_implementations_result_len() -> int:
        if not state.get_implementations_result:
            raise WasmAbortError(
                "__wrap_get_implementations_result_len: get_implementations_result is not set"
            )
        return len(state.get_implementations_result)

    wrap_get_implementations_result_type = FuncType([ValType.i32()], [])

    def wrap_get_implementations_result(ptr: int) -> None:
        if not state.get_implementations_result:
            raise WasmAbortError(
                "__wrap_get_implementations_result: get_implementations_result is not set"
            )
        write_bytes(
            mem.data_ptr(store),
            mem.data_len(store),
            state.get_implementations_result,
            ptr,
        )

    # TODO: use generics or any on wasmtime codebase to fix typings
    linker.define_func("wrap", "__wrap_debug_log", wrap_debug_log_type, wrap_debug_log)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_abort", wrap_abort_type, wrap_abort)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_load_env", wrap_load_env_type, wrap_load_env)  # type: ignore partially unknown

    # invoke
    linker.define_func("wrap", "__wrap_invoke_args", wrap_invoke_args_type, wrap_invoke_args)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_invoke_result", wrap_invoke_result_type, wrap_invoke_result)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_invoke_error", wrap_invoke_error_type, wrap_invoke_error)  # type: ignore partially unknown

    # subinvoke
    linker.define_func("wrap", "__wrap_subinvoke", wrap_subinvoke_type, wrap_subinvoke)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvoke_result_len", wrap_subinvoke_result_len_type, wrap_subinvoke_result_len)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvoke_result", wrap_subinvoke_result_type, wrap_subinvoke_result)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvoke_error_len", wrap_subinvoke_error_len_type, wrap_subinvoke_error_len)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvoke_error", wrap_subinvoke_error_type, wrap_subinvoke_error)  # type: ignore partially unknown

    # subinvoke implementation
    linker.define_func("wrap", "__wrap_subinvokeImplementation", wrap_subinvoke_implementation_type, wrap_subinvoke_implementation)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvokeImplementation_result_len", wrap_subinvoke_implementation_result_len_type, wrap_subinvoke_implementation_result_len)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvokeImplementation_result", wrap_subinvoke_implementation_result_type, wrap_subinvoke_implementation_result)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvokeImplementation_error_len", wrap_subinvoke_implementation_error_len_type, wrap_subinvoke_implementation_error_len)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_subinvokeImplementation_error", wrap_subinvoke_implementation_error_type, wrap_subinvoke_implementation_error)  # type: ignore partially unknown

    # getImplementations
    linker.define_func("wrap", "__wrap_getImplementations", wrap_get_implementations_type, wrap_get_implementations)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_getImplementations_result_len", wrap_get_implementations_result_len_type, wrap_get_implementations_result_len)  # type: ignore partially unknown
    linker.define_func("wrap", "__wrap_getImplementations_result", wrap_get_implementations_result_type, wrap_get_implementations_result)  # type: ignore partially unknown

    # memory
    linker.define("env", "memory", mem)

    instantiated_module = Module(store.engine, module)
    return linker.instantiate(store, instantiated_module)
