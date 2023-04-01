
from pathlib import Path
from polywrap_core import FileReader
from polywrap_uri_resolvers import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, FsUriResolver, SimpleFileReader
from polywrap_client import PolywrapClient, PolywrapClientConfig
from pytest import fixture


@fixture
def client():
    config = PolywrapClientConfig(
            resolver=FsUriResolver(file_reader=SimpleFileReader())
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