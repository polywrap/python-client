"""This module contains the base linker for the Wasm imports."""
from __future__ import annotations

from abc import ABC

from wasmtime import Linker

from ...imports import WrapImports


class BaseWrapLinker(ABC):
    """Base linker for the Wasm imports."""

    linker: Linker
    wrap_imports: WrapImports
