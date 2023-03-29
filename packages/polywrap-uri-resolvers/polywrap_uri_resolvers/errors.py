from dataclasses import asdict
import json
from typing import List, TypeVar
from polywrap_core import IUriResolutionStep, Uri, UriLike

from .utils import get_uri_resolution_path

TUriLike = TypeVar("TUriLike", bound=UriLike)


class UriResolutionError(Exception):
    """Base class for all errors related to URI resolution."""


class InfiniteLoopError(UriResolutionError):
    def __init__(self, uri: Uri, history: List[IUriResolutionStep[TUriLike]]):
        resolution_path = get_uri_resolution_path(history)
        super().__init__(
            f"An infinite loop was detected while resolving the URI: {uri.uri}\n"
            f"History: {json.dumps([asdict(step) for step in resolution_path], indent=2)}"
        )
