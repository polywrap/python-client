from abc import ABC, abstractmethod

from polywrap_result import Result


class IWasmPackage(ABC):
    @abstractmethod
    async def get_wasm_module() -> Result[bytearray]:
        pass
