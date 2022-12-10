from typing import Dict, Union

from polywrap_core import Uri, Wrapper

from .wrapper_cache_interface import IWrapperCache


class WrapperCache(IWrapperCache):
    map: Dict[Uri, Wrapper]

    def __init__(self):
        self.map = {}

    def get(self, uri: Uri) -> Union[Wrapper, None]:
        return self.map.get(uri)

    def set(self, uri: Uri, wrapper: Wrapper) -> None:
        self.map[uri] = wrapper
