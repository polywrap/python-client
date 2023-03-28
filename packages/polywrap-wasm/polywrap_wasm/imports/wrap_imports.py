"""This module contains the WrapImports class that defines\
    all the Wasm imports for the Wrap Wasm module."""
# pylint: disable=too-many-ancestors
from __future__ import annotations

from polywrap_core import Invoker, UriPackageOrWrapper
from wasmtime import Memory, Store

from ..types.state import State
from .abort import WrapAbortImports
from .debug import WrapDebugImports
from .env import WrapEnvImports
from .get_implementations import WrapGetImplementationsImports
from .invoke import WrapInvokeImports
from .subinvoke import WrapSubinvokeImports


class WrapImports(
    WrapAbortImports,
    WrapDebugImports,
    WrapEnvImports,
    WrapGetImplementationsImports,
    WrapInvokeImports,
    WrapSubinvokeImports,
):
    """Wasm imports for the Wrap Wasm module.

    This class is responsible for providing all the Wasm imports to the Wasm module.

    Attributes:
        memory: The Wasm memory instance.
        store: The Wasm store instance.
        state: The state of the Wasm module.
        invoker: The invoker instance.
    """

    def __init__(
        self,
        memory: Memory,
        store: Store,
        state: State,
        invoker: Invoker[UriPackageOrWrapper],
    ) -> None:
        """Initialize the WrapImports instance.

        Args:
            memory: The Wasm memory instance.
            store: The Wasm store instance.
            state: The state of the Wasm module.
            invoker: The invoker instance.
        """
        self.memory = memory
        self.store = store
        self.state = state
        self.invoker = invoker
