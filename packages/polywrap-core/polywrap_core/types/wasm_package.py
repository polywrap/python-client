from abc import ABC, abstractmethod
from typing import Optional

from polywrap_manifest import AnyWrapManifest

from .client import GetManifestOptions
from .wrapper import Wrapper


class IWasmPackage(ABC):
    @abstractmethod
    async def create_wrapper(self) -> Wrapper:
        pass

    @abstractmethod
    async def get_manifest(self, options: Optional[GetManifestOptions] = None) -> AnyWrapManifest:
        pass
