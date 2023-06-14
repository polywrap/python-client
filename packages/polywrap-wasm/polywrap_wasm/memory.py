"""This module contains the create_memory function\
    for creating a shared memory instance for a Wasm module."""
from textwrap import dedent

from wasmtime import Limits, Memory, MemoryType, Store

from .errors import WasmMemoryError


def create_memory(
    store: Store,
    module: bytes,
) -> Memory:
    """Create a host allocated shared memory instance for a Wasm module.

    Args:
        store (Store): The Wasm store.
        module (bytes): The Wasm module.

    Raises:
        WasmMemoryError: if the memory import is not found in the Wasm module.

    Returns:
        Memory: The shared memory instance.
    """
    env_memory_import_signature = bytearray(
        [
            # env ; import module name
            0x65,
            0x6E,
            0x76,
            # string length
            0x06,
            # memory ; import field name
            0x6D,
            0x65,
            0x6D,
            0x6F,
            0x72,
            0x79,
            # import kind
            0x02,
            # limits ; https://github.com/sunfishcode/wasm-reference-manual/blob/master/WebAssembly.md#resizable-limits  # pylint: disable=line-too-long
            # limits ; flags
            # 0x??,
            # limits ; initial
            # 0x__,
        ]
    )
    idx = module.find(env_memory_import_signature)

    if idx < 0:
        raise WasmMemoryError(
            dedent(
                """
                Unable to find Wasm memory import section. \
                Modules must import memory from the "env" module's\
                "memory" field like so:
                (import "env" "memory" (memory (;0;) #))
                """
            )
        )

    memory_inital_limits = module[idx + len(env_memory_import_signature) + 1]

    return Memory(store, MemoryType(Limits(memory_inital_limits, None)))
