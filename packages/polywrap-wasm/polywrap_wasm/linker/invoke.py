"""This module contains the linker for the invoke family of Wasm imports."""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapInvokeLinker(BaseWrapLinker):
    """Linker for the invoke family of Wasm imports."""

    def link_wrap_invoke_args(self) -> None:
        """Link the __wrap_invoke_args function as an import to the Wasm module."""
        wrap_invoke_args_type = FuncType([ValType.i32(), ValType.i32()], [])

        def wrap_invoke_args(ptr: int, length: int) -> None:
            self.wrap_imports.wrap_invoke_args(ptr, length)

        self.linker.define_func(
            "wrap", "__wrap_invoke_args", wrap_invoke_args_type, wrap_invoke_args
        )

    def link_wrap_invoke_result(self) -> None:
        """Link the __wrap_invoke_result function as an import to the Wasm module."""
        wrap_invoke_result_type = FuncType([ValType.i32(), ValType.i32()], [])

        def wrap_invoke_result(ptr: int, length: int) -> None:
            self.wrap_imports.wrap_invoke_result(ptr, length)

        self.linker.define_func(
            "wrap", "__wrap_invoke_result", wrap_invoke_result_type, wrap_invoke_result
        )

    def link_wrap_invoke_error(self) -> None:
        """Link the __wrap_invoke_error function as an import to the Wasm module."""
        wrap_invoke_error_type = FuncType([ValType.i32(), ValType.i32()], [])

        def wrap_invoke_error(ptr: int, length: int) -> None:
            self.wrap_imports.wrap_invoke_error(ptr, length)

        self.linker.define_func(
            "wrap", "__wrap_invoke_error", wrap_invoke_error_type, wrap_invoke_error
        )

    def link_invoke_imports(self) -> None:
        """Link all invoke family of imports to the Wasm module."""
        self.link_wrap_invoke_args()
        self.link_wrap_invoke_result()
        self.link_wrap_invoke_error()
