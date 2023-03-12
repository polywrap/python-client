"""This module contains the imports of the Wasm wrapper module."""
from polywrap_core import Invoker
from wasmtime import FuncType, Instance, Linker, Module, Store, ValType

from .imports import WrapImports
from .memory import create_memory
from .types.state import State


def create_instance(
    store: Store,
    module: bytes,
    state: State,
    invoker: Invoker,
) -> Instance:
    """Create a Wasm instance for a Wasm module.

    Args:
        store: The Wasm store.
        module: The Wasm module.
        state: The state of the Wasm module.
        invoker: The invoker to use for subinvocations.

    Returns:
        Instance: The Wasm instance.
    """
    linker = Linker(store.engine)
    memory = create_memory(store, module)
    wrap_imports = WrapImports(memory, store, state, invoker)

    # Wasm imported function signatures

    wrap_debug_log_type = FuncType(
        [ValType.i32(), ValType.i32()],
        [],
    )

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

    wrap_load_env_type = FuncType([ValType.i32()], [])

    wrap_invoke_args_type = FuncType([ValType.i32(), ValType.i32()], [])

    wrap_invoke_result_type = FuncType([ValType.i32(), ValType.i32()], [])

    wrap_invoke_error_type = FuncType([ValType.i32(), ValType.i32()], [])

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

    wrap_subinvoke_result_len_type = FuncType([], [ValType.i32()])

    wrap_subinvoke_result_type = FuncType([ValType.i32()], [])

    wrap_subinvoke_error_len_type = FuncType([], [ValType.i32()])

    wrap_subinvoke_error_type = FuncType([ValType.i32()], [])

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

    wrap_subinvoke_implementation_result_len_type = FuncType([], [ValType.i32()])

    wrap_subinvoke_implementation_result_type = FuncType([ValType.i32()], [])

    wrap_subinvoke_implementation_error_len_type = FuncType([], [ValType.i32()])

    wrap_subinvoke_implementation_error_type = FuncType([ValType.i32()], [])

    wrap_get_implementations_type = FuncType(
        [ValType.i32(), ValType.i32()], [ValType.i32()]
    )

    wrap_get_implementations_result_len_type = FuncType([], [ValType.i32()])

    wrap_get_implementations_result_type = FuncType([ValType.i32()], [])

    # Wasm imported functions

    def wrap_debug_log(ptr: int, length: int) -> None:
        wrap_imports.wrap_debug_log(ptr, length)

    def wrap_abort(
        ptr: int,
        length: int,
        file_ptr: int,
        file_len: int,
        line: int,
        col: int,
    ) -> None:
        wrap_imports.wrap_abort(ptr, length, file_ptr, file_len, line, col)

    def wrap_load_env(ptr: int) -> None:
        wrap_imports.wrap_load_env(ptr)

    def wrap_invoke_args(ptr: int, length: int) -> None:
        wrap_imports.wrap_invoke_args(ptr, length)

    def wrap_invoke_result(ptr: int, length: int) -> None:
        wrap_imports.wrap_invoke_result(ptr, length)

    def wrap_invoke_error(ptr: int, length: int) -> None:
        wrap_imports.wrap_invoke_error(ptr, length)

    def wrap_subinvoke(
        ptr: int,
        length: int,
        uri_ptr: int,
        uri_len: int,
        args_ptr: int,
        args_len: int,
    ) -> int:
        return wrap_imports.wrap_subinvoke(
            ptr, length, uri_ptr, uri_len, args_ptr, args_len
        )

    def wrap_subinvoke_result_len() -> int:
        return wrap_imports.wrap_subinvoke_result_len()

    def wrap_subinvoke_result(ptr: int) -> None:
        wrap_imports.wrap_subinvoke_result(ptr)

    def wrap_subinvoke_error_len() -> int:
        return wrap_imports.wrap_subinvoke_error_len()

    def wrap_subinvoke_error(ptr: int) -> None:
        wrap_imports.wrap_subinvoke_error(ptr)

    def wrap_subinvoke_implementation(
        ptr: int,
        length: int,
        uri_ptr: int,
        uri_len: int,
        args_ptr: int,
        args_len: int,
        result_ptr: int,
        result_len: int,
    ) -> int:
        return wrap_imports.wrap_subinvoke_implementation(
            ptr,
            length,
            uri_ptr,
            uri_len,
            args_ptr,
            args_len,
            result_ptr,
            result_len,
        )

    def wrap_subinvoke_implementation_result_len() -> int:
        return wrap_imports.wrap_subinvoke_implementation_result_len()

    def wrap_subinvoke_implementation_result(ptr: int) -> None:
        wrap_imports.wrap_subinvoke_implementation_result(ptr)

    def wrap_subinvoke_implementation_error_len() -> int:
        return wrap_imports.wrap_subinvoke_implementation_error_len()

    def wrap_subinvoke_implementation_error(ptr: int) -> None:
        wrap_imports.wrap_subinvoke_implementation_error(ptr)

    def wrap_get_implementations(
        ptr: int,
        length: int,
    ) -> int:
        return wrap_imports.wrap_get_implementations(ptr, length)

    def wrap_get_implementations_result_len() -> int:
        return wrap_imports.wrap_get_implementations_result_len()

    def wrap_get_implementations_result(ptr: int) -> None:
        wrap_imports.wrap_get_implementations_result(ptr)

    # Link Wasm imported functions

    linker.define_func("wrap", "__wrap_debug_log", wrap_debug_log_type, wrap_debug_log)
    linker.define_func("wrap", "__wrap_abort", wrap_abort_type, wrap_abort)
    linker.define_func("wrap", "__wrap_load_env", wrap_load_env_type, wrap_load_env)

    # invoke
    linker.define_func(
        "wrap", "__wrap_invoke_args", wrap_invoke_args_type, wrap_invoke_args
    )
    linker.define_func(
        "wrap", "__wrap_invoke_result", wrap_invoke_result_type, wrap_invoke_result
    )
    linker.define_func(
        "wrap", "__wrap_invoke_error", wrap_invoke_error_type, wrap_invoke_error
    )

    # subinvoke
    linker.define_func("wrap", "__wrap_subinvoke", wrap_subinvoke_type, wrap_subinvoke)
    linker.define_func(
        "wrap",
        "__wrap_subinvoke_result_len",
        wrap_subinvoke_result_len_type,
        wrap_subinvoke_result_len,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvoke_result",
        wrap_subinvoke_result_type,
        wrap_subinvoke_result,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvoke_error_len",
        wrap_subinvoke_error_len_type,
        wrap_subinvoke_error_len,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvoke_error",
        wrap_subinvoke_error_type,
        wrap_subinvoke_error,
    )

    # subinvoke implementation
    linker.define_func(
        "wrap",
        "__wrap_subinvokeImplementation",
        wrap_subinvoke_implementation_type,
        wrap_subinvoke_implementation,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvokeImplementation_result_len",
        wrap_subinvoke_implementation_result_len_type,
        wrap_subinvoke_implementation_result_len,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvokeImplementation_result",
        wrap_subinvoke_implementation_result_type,
        wrap_subinvoke_implementation_result,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvokeImplementation_error_len",
        wrap_subinvoke_implementation_error_len_type,
        wrap_subinvoke_implementation_error_len,
    )
    linker.define_func(
        "wrap",
        "__wrap_subinvokeImplementation_error",
        wrap_subinvoke_implementation_error_type,
        wrap_subinvoke_implementation_error,
    )

    # getImplementations
    linker.define_func(
        "wrap",
        "__wrap_getImplementations",
        wrap_get_implementations_type,
        wrap_get_implementations,
    )
    linker.define_func(
        "wrap",
        "__wrap_getImplementations_result_len",
        wrap_get_implementations_result_len_type,
        wrap_get_implementations_result_len,
    )
    linker.define_func(
        "wrap",
        "__wrap_getImplementations_result",
        wrap_get_implementations_result_type,
        wrap_get_implementations_result,
    )

    # memory
    linker.define(store, "env", "memory", memory)

    instantiated_module = Module(store.engine, module)
    return linker.instantiate(store, instantiated_module)
