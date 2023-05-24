"""This module contains the base class for the wrap imports modules."""
from __future__ import annotations

from abc import ABC
from typing import Optional

from polywrap_core import Invoker
from wasmtime import Memory, Store

from ...buffer import read_bytes, read_string, write_bytes, write_string
from ...types.state import State


class BaseWrapImports(ABC):
    """Base class for the wrap imports modules."""

    memory: Memory
    store: Store
    state: State
    invoker: Optional[Invoker]

    def read_string(self, ptr: int, length: int) -> str:
        """Read a UTF-8 encoded string from the memory buffer."""
        return read_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            ptr,
            length,
        )

    def read_bytes(self, ptr: int, length: int) -> bytes:
        """Read bytes from the memory buffer."""
        return read_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            ptr,
            length,
        )

    def write_string(self, ptr: int, value: str) -> None:
        """Write a UTF-8 encoded string to the given pointer in the memory buffer."""
        write_string(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            value,
            ptr,
        )

    def write_bytes(self, ptr: int, value: bytes) -> None:
        """Write bytes to the given pointer in the memory buffer."""
        write_bytes(
            self.memory.data_ptr(self.store),
            self.memory.data_len(self.store),
            value,
            ptr,
        )
