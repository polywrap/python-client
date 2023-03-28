"""This module contains the linker for the debug family of Wasm imports."""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapDebugLinker(BaseWrapLinker):
    """Linker for the debug family of Wasm imports."""

    def link_wrap_debug_log(self) -> None:
        """Link the __wrap_debug_log function as an import to the Wasm module."""
        wrap_debug_log_type = FuncType(
            [ValType.i32(), ValType.i32()],
            [],
        )

        def wrap_debug_log(ptr: int, length: int) -> None:
            self.wrap_imports.wrap_debug_log(ptr, length)

        self.linker.define_func(
            "wrap", "__wrap_debug_log", wrap_debug_log_type, wrap_debug_log
        )

    def link_debug_imports(self) -> None:
        """Link all debug family of imports to the Wasm module."""
        self.link_wrap_debug_log()
