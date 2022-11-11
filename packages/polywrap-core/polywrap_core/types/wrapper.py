from abc import abstractmethod
from typing import Dict, Union

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .core_client import GetFileOptions
from .invoke import Invocable, InvocableResult, InvokeOptions, Invoker


class Wrapper(Invocable):
    """
    Invoke the Wrapper based on the provided [[InvokeOptions]]

    Args:
        options: Options for this invocation.
        client: The client instance requesting this invocation. This client will be used for any sub-invokes that occur.
    """

    @abstractmethod
    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        pass

    @abstractmethod
    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        pass

    @abstractmethod
    def get_manifest(self) -> Result[AnyWrapManifest]:
        pass


WrapperCache = Dict[str, Wrapper]
