from typing import List
from polywrap_core import Uri, IUriResolutionStep

class InfiniteLoopError(Exception):
    def __init__(self, uri: Uri, history: List[IUriResolutionStep]):
        # TODO: Add history with get_resolution_stack
        self.message = f"An infinite loop was detected while resolving the URI: {uri.uri}"