"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Any, Dict
from .uri import Uri

@dataclass(slots=True, kw_only=True)
class Env:
    """
    this type can be used to set env for a wrapper in the client

    Args:
        uri: Uri of wrapper
        env: env variables used by the module
    """
    uri: Uri
    env: Dict[str, Any] = ...

