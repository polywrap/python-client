from abc import ABC, abstractmethod
from typing import Union

from polywrap_core import Uri, Wrapper


class IWrapperCache(ABC):
    @abstractmethod
    def get(self, uri: Uri) -> Union[Wrapper, None]:
        pass

    @abstractmethod
    def set(self, uri: Uri, wrapper: Wrapper) -> None:
        pass
