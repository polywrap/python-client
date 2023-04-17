
from pathlib import Path
from polywrap_core import FileReader, ClientConfig, Invoker, UriPackageOrWrapper, Env, Uri
from polywrap_uri_resolvers import (
    RecursiveResolver,
    UriResolverAggregator,
    StaticResolver,
    FsUriResolver,
    SimpleFileReader,
    WRAP_MANIFEST_PATH,
    WRAP_MODULE_PATH
)
from polywrap_plugin import PluginModule, PluginPackage
from pytest import fixture
from typing import Dict, Any, Optional
from polywrap_client import PolywrapClient
import time

@fixture
def client(memory_storage_plugin: PluginPackage[None]):
    memory_storage_uri = Uri.from_str("wrap://ens/memory-storage.polywrap.eth")
    config = ClientConfig(
        resolver=RecursiveResolver(
            UriResolverAggregator(
                [
                    FsUriResolver(file_reader=SimpleFileReader()),
                    StaticResolver({ memory_storage_uri: memory_storage_plugin})
                ]
            )
        )
    )
    return PolywrapClient(config)

@fixture
def simple_wrap_module():
    wrap_path = Path(__file__).parent / "cases" / "simple-invoke" / "wrap.wasm"
    with open(wrap_path, "rb") as f:
        yield f.read()


@fixture
def simple_wrap_manifest():
    wrap_path = Path(__file__).parent / "cases" / "simple-invoke" / "wrap.info"
    with open(wrap_path, "rb") as f:
        yield f.read()

@fixture
def simple_file_reader(simple_wrap_module: bytes, simple_wrap_manifest: bytes):
    class SimpleFileReader(FileReader):
        async def read_file(self, file_path: str) -> bytes:
            if file_path == WRAP_MODULE_PATH:
                return simple_wrap_module
            if file_path == WRAP_MANIFEST_PATH:
                return simple_wrap_manifest
            raise FileNotFoundError(f"FileNotFound: {file_path}")

    yield SimpleFileReader()

class MemoryStorage(PluginModule[None]):
    def __init__(self):
        super().__init__(None)
        self.value = 0

    def getData(self, args: Dict[str, Any], client: Invoker[UriPackageOrWrapper], env: Optional[Env]) -> int:
        time.sleep(0.05)  # Sleep for 50 milliseconds
        return self.value

    def setData(self, args: Dict[str, Any], client: Invoker[UriPackageOrWrapper], env: Optional[Env]) -> bool:
        time.sleep(0.05)  # Sleep for 50 milliseconds
        self.value = args["value"]
        return True


@fixture
def memory_storage_plugin() -> PluginPackage[None]:
    return PluginPackage(module=MemoryStorage(), manifest={})  # type: ignore


class Adder(PluginModule[None]):
    def add(self, args: Dict[str, Any], client: Invoker[UriPackageOrWrapper], env: Optional[Env]) -> int:
        return args["a"] + args["b"]


@fixture
def adder_plugin() -> PluginPackage[None]:
    return PluginPackage(module=Adder(None), manifest={})  # type: ignore
