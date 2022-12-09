from typing import List
from polywrap_core import Uri, IUriResolutionStep
from dataclasses import asdict
import json

from ..helpers.get_uri_resolution_path import get_uri_resolution_path


class InfiniteLoopError(Exception):
    def __init__(self, uri: Uri, history: List[IUriResolutionStep]):
        super().__init__(
            f"An infinite loop was detected while resolving the URI: {uri.uri}\n"
            f"History: {json.dumps(asdict(get_uri_resolution_path(history)), indent=2)}"
        )
