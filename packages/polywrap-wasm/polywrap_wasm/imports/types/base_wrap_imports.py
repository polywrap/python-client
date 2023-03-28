from __future__ import annotations

from abc import ABC
from wasmtime import Memory, Store
from polywrap_core import Invoker, UriPackageOrWrapper

from ...types.state import State
from ...buffer import read_bytes, read_string, write_bytes, write_string


class BaseWrapImports(ABC):
    memory: Memory
    store: Store
    state: State
    invoker: Invoker[UriPackageOrWrapper]

    def read_string(self, ptr: int, length: int) -> str:
        return read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            ptr,
            length,
        )

    def read_bytes(self, ptr: int, length: int) -> bytes:
        return read_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            ptr,
            length,
        )

    def write_string(self, ptr: int, value: str) -> None:
        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            value,
            ptr,
        )
    
    def write_bytes(self, ptr: int, value: bytes) -> None:
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            value,
            ptr,
        )
