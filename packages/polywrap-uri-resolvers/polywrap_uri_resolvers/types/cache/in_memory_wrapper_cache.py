from typing import Dict, Union

from polywrap_core import Uri, Wrapper, UriPackageOrWrapper

from .wrapper_cache import WrapperCache


class InMemoryWrapperCache(WrapperCache):
    map: Dict[Uri, Wrapper[UriPackageOrWrapper]]

    def __init__(self):
        self.map = {}

    def get(self, uri: Uri) -> Union[Wrapper[UriPackageOrWrapper], None]:
        return self.map.get(uri)

    def set(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]) -> None:
        self.map[uri] = wrapper
