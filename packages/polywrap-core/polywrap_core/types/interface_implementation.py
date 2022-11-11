from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .uri import Uri

# TODO:  Should we remove this interfaceimplementation?
@dataclass(slots=True, kw_only=True)
class InterfaceImplementations:
    interface: Uri
    implementations: List[Uri]
