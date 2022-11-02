from abc import ABC, abstractmethod
from typing import Optional

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .client import GetManifestOptions
from .wrapper import Wrapper


class IWrapPackage(ABC):
    @abstractmethod
    async def create_wrapper(self) -> Result[Wrapper]:
        pass

    @abstractmethod
    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        pass
