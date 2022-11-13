from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from polywrap_result import Result

from .uri import Uri

if TYPE_CHECKING:
    from .uri_package_wrapper import UriPackageOrWrapper


@dataclass(slots=True, kw_only=True)
class IUriResolutionStep:
    source_uri: Uri
    result: Result["UriPackageOrWrapper"]
    description: Optional[str] = None
    sub_history: Optional[List["IUriResolutionStep"]] = None
