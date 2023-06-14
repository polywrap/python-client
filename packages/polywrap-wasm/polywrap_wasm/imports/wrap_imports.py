"""This module contains the WrapImports class that defines\
    all the Wasm imports for the Wrap Wasm module."""
# pylint: disable=too-many-ancestors
from __future__ import annotations

from typing import Optional

from polywrap_core import Invoker
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

    Args:
        memory (Memory): The Wasm memory instance.
        store (Store): The Wasm store instance.
        state (State): The state of the Wasm module.
        invoker (Invoker): The invoker instance.

    Attributes:
        memory (Memory): The Wasm memory instance.
        store (Store): The Wasm store instance.
        state (State): The state of the Wasm module.
        invoker (Invoker): The invoker instance.
    """

    def __init__(
        self,
        memory: Memory,
        store: Store,
        state: State,
        invoker: Optional[Invoker],
    ) -> None:
        """Initialize the WrapImports instance."""
        self.memory = memory
        self.store = store
        self.state = state
        self.invoker = invoker
