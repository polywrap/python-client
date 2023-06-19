import time
from typing import Any, Callable, Dict
from polywrap_test_cases import get_path_to_test_wrappers

import pytest
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri
from polywrap_plugin import PluginModule, PluginPackage
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


class MemoryStoragePlugin(PluginModule[None]):
    def __init__(self):
        super().__init__(None)
        self._value = None

    def getData(self, *_: Any) -> Any:
        self.sleep(0.005)
        return self._value

    def setData(self, args: Dict[str, Any], *_:Any) -> bool:
        self.sleep(0.005)
        self._value = args["value"]
        return True

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


def memory_storage_plugin() -> PluginPackage[None]:
    return PluginPackage(manifest=NotImplemented, module=MemoryStoragePlugin())


@pytest.fixture
def wrapper_uri() -> Callable[[str], Uri]:
    def get_subinvoke_wrapper_uri(implementation: str) -> Uri:
        subinvoke_wrapper_path = f"{get_path_to_test_wrappers()}/asyncify/implementations/{implementation}"
        return Uri.from_str(f"file/{subinvoke_wrapper_path}")

    return get_subinvoke_wrapper_uri


@pytest.fixture
def builder() -> ClientConfigBuilder:
    return (
        PolywrapClientConfigBuilder()
        .set_package(
            Uri.from_str("ens/memory-storage.polywrap.eth"),
            memory_storage_plugin(),
        )
        .add_resolver(FsUriResolver(SimpleFileReader()))
    )

