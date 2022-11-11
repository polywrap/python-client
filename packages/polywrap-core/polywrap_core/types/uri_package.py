from __future__ import annotations

from dataclasses import dataclass

from .uri import Uri
from .wasm_package import IWrapPackage


@dataclass(slots=True, kw_only=True)
class UriPackage:
    uri: Uri
    package: IWrapPackage
