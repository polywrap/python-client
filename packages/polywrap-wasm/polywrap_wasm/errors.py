"""This module contains the error classes used by polywrap-wasm package."""
from polywrap_core import WrapError


class WasmError(WrapError):
    """Base class for all exceptions related to wasm wrappers."""


class WasmExportNotFoundError(WasmError):
    """Raises when an export isn't found in the wasm module."""


class WasmMemoryError(WasmError):
    """Raises when the Wasm memory is not found."""


__all__ = [
    "WasmError",
    "WasmExportNotFoundError",
    "WasmMemoryError",
]
