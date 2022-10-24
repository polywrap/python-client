from dataclasses import dataclass
from typing import List

from .uri import Uri

@dataclass(slots=True, kw_only=True)
class InterfaceImplementations:
    interface: Uri
    implementations: List[Uri]
