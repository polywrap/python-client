from typing import Any, List, cast
import pytest

from pathlib import Path

from polywrap_msgpack import msgpack_decode
from polywrap_core import Uri, InvokeOptions, Invoker, InvokerOptions, UriPackageOrWrapper
from polywrap_wasm import FileReader, WasmPackage, WasmWrapper, WRAP_MODULE_PATH
from polywrap_manifest import deserialize_wrap_manifest

from polywrap_wasm.constants import WRAP_MANIFEST_PATH

@pytest.fixture
def mock_invoker():
    class MockInvoker(Invoker[UriPackageOrWrapper]):
        async def invoke(self, options: InvokerOptions[UriPackageOrWrapper]) -> Any:
            raise NotImplementedError()
        
        def get_implementations(self, uri: Uri) -> List[Uri]:
            raise NotImplementedError()

    return MockInvoker()


@pytest.fixture
def simple_wrap_module():
    wrap_path = Path(__file__).parent / "cases" / "simple" / "wrap.wasm"
    with open(wrap_path, "rb") as f:
        yield f.read()


@pytest.fixture
def simple_wrap_manifest():
    wrap_path = Path(__file__).parent / "cases" / "simple" / "wrap.info"
    with open(wrap_path, "rb") as f:
        yield f.read()


@pytest.fixture
def dummy_file_reader():
    class DummyFileReader(FileReader):
        async def read_file(self, file_path: str) -> bytes:
            raise NotImplementedError()

    yield DummyFileReader()


@pytest.fixture
def simple_file_reader(simple_wrap_module: bytes, simple_wrap_manifest: bytes):
    class DummyFileReader(FileReader):
        async def read_file(self, file_path: str) -> bytes:
            if file_path == WRAP_MODULE_PATH:
                return simple_wrap_module
            if file_path == WRAP_MANIFEST_PATH:
                return simple_wrap_manifest
            raise NotImplementedError()

    yield DummyFileReader()


@pytest.mark.asyncio
async def test_invoke_with_wrapper(
    dummy_file_reader: FileReader, simple_wrap_module: bytes, simple_wrap_manifest: bytes, mock_invoker: Invoker[UriPackageOrWrapper]
):
    wrapper = WasmWrapper(dummy_file_reader, simple_wrap_module, deserialize_wrap_manifest(simple_wrap_manifest))

    message = "hey"
    args = {"arg": message}
    options: InvokeOptions[UriPackageOrWrapper] = InvokeOptions(uri=Uri.from_str("fs/./build"), method="simpleMethod", args=args)
    result = await wrapper.invoke(options, mock_invoker)
    assert result.encoded is True
    assert msgpack_decode(cast(bytes, result.result)) == message


@pytest.mark.asyncio
async def test_invoke_with_package(simple_file_reader: FileReader, mock_invoker: Invoker[UriPackageOrWrapper]):
    package = WasmPackage(simple_file_reader)
    wrapper = await package.create_wrapper()

    message = "hey"
    args = {"arg": message}
    options: InvokeOptions[UriPackageOrWrapper] = InvokeOptions(uri=Uri.from_str("fs/./build"), method="simpleMethod", args=args)
    result = await wrapper.invoke(options, mock_invoker)
    assert result.encoded is True
    assert msgpack_decode(cast(bytes, result.result)) == message
