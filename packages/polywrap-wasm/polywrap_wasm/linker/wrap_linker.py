"""This module contains the linker for all wrap imports."""
# pylint: disable=too-many-ancestors
from wasmtime import Linker

from ..imports import WrapImports
from .abort import WrapAbortLinker
from .debug import WrapDebugLinker
from .env import WrapEnvLinker
from .get_implementations import WrapGetImplementationsLinker
from .invoke import WrapInvokeLinker
from .subinvoke import WrapSubinvokeLinker
from .subinvoke_implementation import WrapSubinvokeImplementationLinker


class WrapLinker(
    WrapAbortLinker,
    WrapDebugLinker,
    WrapEnvLinker,
    WrapGetImplementationsLinker,
    WrapInvokeLinker,
    WrapSubinvokeLinker,
    WrapSubinvokeImplementationLinker,
):
    """Linker for the Wrap Wasm module.

    This class is responsible for linking all the Wasm imports to the Wasm module.

    Args:
        linker: The Wasm linker instance.
        wrap_imports: The Wasm imports instance.

    Attributes:
        linker: The Wasm linker instance.
        wrap_imports: The Wasm imports instance.
    """

    def __init__(self, linker: Linker, wrap_imports: WrapImports) -> None:
        """Initialize the WrapLinker instance."""
        self.linker = linker
        self.wrap_imports = wrap_imports

    def link(self) -> None:
        """Link all the Wasm imports to the Wasm module."""
        self.link_abort_imports()
        self.link_debug_imports()
        self.link_env_imports()
        self.link_get_implementations_imports()
        self.link_invoke_imports()
        self.link_subinvoke_imports()
        self.link_subinvoke_implementation_imports()
