from abc import ABC, abstractmethod
from typing import Union

from polywrap_core import Uri, Wrapper, UriPackageOrWrapper


class WrapperCache(ABC):
    @abstractmethod
    def get(self, uri: Uri) -> Union[Wrapper[UriPackageOrWrapper], None]:
        pass

    @abstractmethod
    def set(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]) -> None:
        pass
