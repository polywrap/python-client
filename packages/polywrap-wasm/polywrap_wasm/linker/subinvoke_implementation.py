"""This module contains the linker for the subinvoke implementation family of Wasm imports."""
# pylint: disable=unused-argument
# pylint: disable=duplicate-code
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapSubinvokeImplementationLinker(BaseWrapLinker):
    """Linker for the subinvoke implementation family of Wasm imports."""

    def link_wrap_subinvoke_implementation(
        self,
    ) -> None:
        """Link the __wrap_subinvoke_implementation function as an import to the Wasm module."""
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
            ptr: int,
            length: int,
            uri_ptr: int,
            uri_len: int,
            args_ptr: int,
            args_len: int,
            result_ptr: int,
            result_len: int,
        ) -> int:
            return self.wrap_imports.wrap_subinvoke(
                uri_ptr,
                uri_len,
                args_ptr,
                args_len,
                result_ptr,
                result_len,
            )

        self.linker.define_func(
            "wrap",
            "__wrap_subinvokeImplementation",
            wrap_subinvoke_implementation_type,
            wrap_subinvoke_implementation,
        )

    def link_wrap_subinvoke_implementation_result_len(self) -> None:
        """Link the __wrap_subinvoke_implementation_result_len function\
            as an import to the Wasm module."""
        wrap_subinvoke_implementation_result_len_type = FuncType([], [ValType.i32()])

        def wrap_subinvoke_implementation_result_len() -> int:
            return self.wrap_imports.wrap_subinvoke_result_len()

        self.linker.define_func(
            "wrap",
            "__wrap_subinvokeImplementation_result_len",
            wrap_subinvoke_implementation_result_len_type,
            wrap_subinvoke_implementation_result_len,
        )

    def link_wrap_subinvoke_implementation_result(self) -> None:
        """Link the __wrap_subinvoke_implementation_result function\
            as an import to the Wasm module."""
        wrap_subinvoke_implementation_result_type = FuncType([ValType.i32()], [])

        def wrap_subinvoke_implementation_result(ptr: int) -> None:
            self.wrap_imports.wrap_subinvoke_result(ptr)

        self.linker.define_func(
            "wrap",
            "__wrap_subinvokeImplementation_result",
            wrap_subinvoke_implementation_result_type,
            wrap_subinvoke_implementation_result,
        )

    def link_wrap_subinvoke_implementation_error_len(self) -> None:
        """Link the __wrap_subinvoke_implementation_error_len function\
            as an import to the Wasm module."""
        wrap_subinvoke_implementation_error_len_type = FuncType([], [ValType.i32()])

        def wrap_subinvoke_implementation_error_len() -> int:
            return self.wrap_imports.wrap_subinvoke_error_len()

        self.linker.define_func(
            "wrap",
            "__wrap_subinvokeImplementation_error_len",
            wrap_subinvoke_implementation_error_len_type,
            wrap_subinvoke_implementation_error_len,
        )

    def link_wrap_subinvoke_implementation_error(self) -> None:
        """Link the __wrap_subinvokeImplementation_error function\
            as an import to the Wasm module."""
        wrap_subinvoke_implementation_error_type = FuncType([ValType.i32()], [])

        def wrap_subinvoke_implementation_error(ptr: int) -> None:
            self.wrap_imports.wrap_subinvoke_error(ptr)

        self.linker.define_func(
            "wrap",
            "__wrap_subinvokeImplementation_error",
            wrap_subinvoke_implementation_error_type,
            wrap_subinvoke_implementation_error,
        )

    def link_subinvoke_implementation_imports(self) -> None:
        """Link all subinvoke_implementation imports."""
        self.link_wrap_subinvoke_implementation()
        self.link_wrap_subinvoke_implementation_result_len()
        self.link_wrap_subinvoke_implementation_result()
        self.link_wrap_subinvoke_implementation_error_len()
        self.link_wrap_subinvoke_implementation_error()
