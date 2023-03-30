"""This module contains the linker for the get_implementations family of Wasm imports."""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapGetImplementationsLinker(BaseWrapLinker):
    """Linker for the get_implementations family of Wasm imports."""

    def link_wrap_get_implementations(self) -> None:
        """Link the __wrap_get_implementations function as an import to the Wasm module."""
        wrap_get_implementations_type = FuncType(
            [
                ValType.i32(),
                ValType.i32(),
            ],
            [
                ValType.i32(),
            ],
        )

        def wrap_get_implementations(
            uri_ptr: int,
            uri_len: int,
        ) -> bool:
            return self.wrap_imports.wrap_get_implementations(uri_ptr, uri_len)

        self.linker.define_func(
            "wrap",
            "__wrap_getImplementations",
            wrap_get_implementations_type,
            wrap_get_implementations,
        )

    def link_wrap_get_implementations_result_len(self) -> None:
        """Link the __wrap_get_implementations_result_len function\
            as an import to the Wasm module."""
        wrap_get_implementations_result_len_type = FuncType(
            [],
            [
                ValType.i32(),
            ],
        )

        def wrap_get_implementations_result_len() -> int:
            return self.wrap_imports.wrap_get_implementations_result_len()

        self.linker.define_func(
            "wrap",
            "__wrap_getImplementations_result_len",
            wrap_get_implementations_result_len_type,
            wrap_get_implementations_result_len,
        )

    def link_wrap_get_implementations_result(self) -> None:
        """Link the __wrap_get_implementations_result function as an import to the Wasm module."""
        wrap_get_implementations_result_type = FuncType(
            [
                ValType.i32(),
            ],
            [],
        )

        def wrap_get_implementations_result(
            ptr: int,
        ) -> None:
            self.wrap_imports.wrap_get_implementations_result(ptr)

        self.linker.define_func(
            "wrap",
            "__wrap_getImplementations_result",
            wrap_get_implementations_result_type,
            wrap_get_implementations_result,
        )

    def link_get_implementations_imports(self) -> None:
        """Link all get_implementations imports to the Wasm module."""
        self.link_wrap_get_implementations()
        self.link_wrap_get_implementations_result_len()
        self.link_wrap_get_implementations_result()
