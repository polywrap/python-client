"""This module contains the embedded wraps for the system configuration bundle."""

from pathlib import Path

from polywrap_core import WrapPackage
from polywrap_wasm import WasmPackage

from .embedded_file_reader import EmbeddedFileReader


def get_embedded_wrap(name: str) -> WrapPackage:
    """Get the embedded wrap with the given name."""
    embedded_wrap_path = Path(__file__).parent / name
    return WasmPackage(EmbeddedFileReader(embedded_wrap_path))


__all__ = ["get_embedded_wrap"]
