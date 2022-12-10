from abc import ABC, abstractmethod

from polywrap_result import Result

from .wrap_package import IWrapPackage


class IWasmPackage(IWrapPackage, ABC):
    @abstractmethod
    async def get_wasm_module(self) -> Result[bytes]:
        pass
