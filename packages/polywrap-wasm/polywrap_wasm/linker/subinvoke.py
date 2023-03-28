"""This module contains the linker for the subinvoke family of Wasm imports."""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapSubinvokeLinker(BaseWrapLinker):
    """Linker for the subinvoke family of Wasm imports."""

    def link_wrap_subinvoke(
        self,
    ) -> None:
        """Link the __wrap_subinvoke function as an import to the Wasm module."""
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
            ptr: int,
            length: int,
            uri_ptr: int,
            uri_len: int,
            args_ptr: int,
            args_len: int,
        ) -> int:
            return self.wrap_imports.wrap_subinvoke(
                ptr, length, uri_ptr, uri_len, args_ptr, args_len
            )

        self.linker.define_func(
            "wrap", "__wrap_subinvoke", wrap_subinvoke_type, wrap_subinvoke
        )

    def link_wrap_subinvoke_result_len(self) -> None:
        """Link the __wrap_subinvoke_result_len function as an import to the Wasm module."""
        wrap_subinvoke_result_len_type = FuncType([], [ValType.i32()])

        def wrap_subinvoke_result_len() -> int:
            return self.wrap_imports.wrap_subinvoke_result_len()

        self.linker.define_func(
            "wrap",
            "__wrap_subinvoke_result_len",
            wrap_subinvoke_result_len_type,
            wrap_subinvoke_result_len,
        )

    def link_wrap_subinvoke_result(self) -> None:
        """Link the __wrap_subinvoke_result function as an import to the Wasm module."""
        wrap_subinvoke_result_type = FuncType([ValType.i32()], [])

        def wrap_subinvoke_result(ptr: int) -> None:
            self.wrap_imports.wrap_subinvoke_result(ptr)

        self.linker.define_func(
            "wrap",
            "__wrap_subinvoke_result",
            wrap_subinvoke_result_type,
            wrap_subinvoke_result,
        )

    def link_wrap_subinvoke_error_len(self) -> None:
        """Link the __wrap_subinvoke_error_len function as an import to the Wasm module."""
        wrap_subinvoke_error_len_type = FuncType([], [ValType.i32()])

        def wrap_subinvoke_error_len() -> int:
            return self.wrap_imports.wrap_subinvoke_error_len()

        self.linker.define_func(
            "wrap",
            "__wrap_subinvoke_error_len",
            wrap_subinvoke_error_len_type,
            wrap_subinvoke_error_len,
        )

    def link_wrap_subinvoke_error(self) -> None:
        """Link the __wrap_subinvoke_error function as an import to the Wasm module."""
        wrap_subinvoke_error_type = FuncType([ValType.i32()], [])

        def wrap_subinvoke_error(ptr: int) -> None:
            self.wrap_imports.wrap_subinvoke_error(ptr)

        self.linker.define_func(
            "wrap",
            "__wrap_subinvoke_error",
            wrap_subinvoke_error_type,
            wrap_subinvoke_error,
        )

    def link_subinvoke_imports(self) -> None:
        """Link all subinvoke imports."""
        self.link_wrap_subinvoke()
        self.link_wrap_subinvoke_result_len()
        self.link_wrap_subinvoke_result()
        self.link_wrap_subinvoke_error_len()
        self.link_wrap_subinvoke_error()
