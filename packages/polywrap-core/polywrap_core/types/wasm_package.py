"""This module contains the IWasmPackage interface."""
from abc import ABC, abstractmethod

from polywrap_result import Result

from .wrap_package import IWrapPackage


class IWasmPackage(IWrapPackage, ABC):
    """Wasm package interface."""

    @abstractmethod
    async def get_wasm_module(self) -> Result[bytes]:
        """Get the wasm module from the Wasm wrapper package.

        Returns:
            Result[bytes]: The wasm module or an error.
        """
