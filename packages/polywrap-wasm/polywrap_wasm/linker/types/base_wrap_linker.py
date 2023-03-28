from __future__ import annotations

from abc import ABC
from wasmtime import Linker

from ...imports import WrapImports


class BaseWrapLinker(ABC):
    linker: Linker
    wrap_imports: WrapImports
