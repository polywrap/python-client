"""This module contains the linker for the abort family of Wasm imports."""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapAbortLinker(BaseWrapLinker):
    """Linker for the abort family of Wasm imports."""

    def link_wrap_abort(self) -> None:
        """Link the __wrap_abort function as an import to the Wasm module."""
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
            ptr: int,
            length: int,
            file_ptr: int,
            file_len: int,
            line: int,
            col: int,
        ) -> None:
            self.wrap_imports.wrap_abort(ptr, length, file_ptr, file_len, line, col)

        self.linker.define_func("wrap", "__wrap_abort", wrap_abort_type, wrap_abort)

    def link_abort_imports(self) -> None:
        """Link all abort family of imports to the Wasm module."""
        self.link_wrap_abort()
