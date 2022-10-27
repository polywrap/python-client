from typing import List, Optional

from polywrap_result import Err, Ok, Result

from ..types import (
    IUriResolutionStep,
    IWasmPackage,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriWrapper,
    Wrapper,
)


class UriResolutionResult:
    result: Result[UriPackageOrWrapper]
    history: Optional[List[IUriResolutionStep]]

    @staticmethod
    def ok(
        uri: Uri,
        package: Optional[IWasmPackage] = None,
        wrapper: Optional[Wrapper] = None,
    ) -> Result[UriPackageOrWrapper]:
        if wrapper:
            return Ok(UriWrapper(uri=uri, wrapper=wrapper))
        elif package:
            return Ok(UriPackage(uri=uri, package=package))
        else:
            return Ok(uri)

    @staticmethod
    def err(error: Exception) -> Result[UriPackageOrWrapper]:
        return Err(error)
