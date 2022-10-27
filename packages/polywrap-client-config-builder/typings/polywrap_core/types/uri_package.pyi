"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from .uri import Uri
from .wasm_package import IWasmPackage

@dataclass(slots=True, kw_only=True)
class UriPackage:
    uri: Uri
    package: IWasmPackage
    ...


