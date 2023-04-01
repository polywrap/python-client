"""This module contains the linker for the env family of Wasm imports.""" ""
from wasmtime import FuncType, ValType

from .types import BaseWrapLinker


class WrapEnvLinker(BaseWrapLinker):
    """Linker for the env family of Wasm imports."""

    def link_wrap_load_env(self) -> None:
        """Link the __wrap_load_env function as an import to the Wasm module."""
        wrap_load_env_type = FuncType(
            [ValType.i32()],
            [],
        )

        def wrap_load_env(ptr: int) -> None:
            self.wrap_imports.wrap_load_env(ptr)

        self.linker.define_func(
            "wrap", "__wrap_load_env", wrap_load_env_type, wrap_load_env
        )

    def link_env_imports(self) -> None:
        """Link all env family of imports to the Wasm module."""
        self.link_wrap_load_env()
