"""This module contains the imports of the Wasm wrapper module."""
from typing import Optional

from polywrap_core import Invoker
from wasmtime import Instance, Linker, Module, Store

from .imports import WrapImports
from .linker import WrapLinker
from .memory import create_memory
from .types.state import State


def create_instance(
    store: Store,
    module: bytes,
    state: State,
    invoker: Optional[Invoker],
) -> Instance:
    """Create a Wasm instance for a Wasm module.

    Args:
        store (Store): The Wasm store.
        module (bytes): The Wasm module.
        state (State): The state of the Wasm module.
        invoker (Optional[Invoker]): The invoker to use for subinvocations.

    Returns:
        Instance: The Wasm instance.
    """
    linker = Linker(store.engine)
    memory = create_memory(store, module)

    # Link memory
    linker.define(store, "env", "memory", memory)

    wrap_imports = WrapImports(memory, store, state, invoker)
    wrap_linker = WrapLinker(linker, wrap_imports)
    wrap_linker.link()

    instantiated_module = Module(store.engine, module)
    return linker.instantiate(store, instantiated_module)
