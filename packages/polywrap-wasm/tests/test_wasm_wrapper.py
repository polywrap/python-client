from typing import List
import pytest

from pathlib import Path

from polywrap_msgpack import msgpack_decode
from polywrap_core import Uri, InvokeOptions, Invoker, InvokerOptions, InvokeResult
from polywrap_wasm import IFileReader, WasmPackage, WasmWrapper, WRAP_MODULE_PATH
from polywrap_manifest import deserialize_wrap_manifest, AnyWrapManifest

from polywrap_wasm.constants import WRAP_MANIFEST_PATH

from result import Result, Err

@pytest.fixture
def mock_invoker():
    class MockInvoker(Invoker):
        async def invoke(self, options: InvokerOptions) -> InvokeResult:
            return InvokeResult()
        
        def get_implementations(self, uri: Uri) -> Result[List[Uri], Exception]:
            return Err(NotImplementedError())

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
    class FileReader(IFileReader):
        async def read_file(self, file_path: str) -> bytes:
            return b""

    yield FileReader()


@pytest.fixture
def simple_file_reader(simple_wrap_module: bytes, simple_wrap_manifest: bytes):
    class FileReader(IFileReader):
        async def read_file(self, file_path: str) -> bytes:
            if file_path == WRAP_MODULE_PATH:
                return simple_wrap_module
            if file_path == WRAP_MANIFEST_PATH:
                return simple_wrap_manifest
            raise FileNotFoundError(file_path)

    yield FileReader()


@pytest.mark.asyncio
async def test_invoke_with_wrapper(
    dummy_file_reader: IFileReader, simple_wrap_module: bytes, simple_wrap_manifest: bytes, mock_invoker: Invoker
):
    wrapper = WasmWrapper(dummy_file_reader, simple_wrap_module, deserialize_wrap_manifest(simple_wrap_manifest))

    message = "hey"
    args = {"arg": message}
    options = InvokeOptions(uri=Uri("fs/./build"), method="simpleMethod", args=args)
    result = await wrapper.invoke(options, mock_invoker) 
    assert msgpack_decode(result.result) == message  # type: ignore


@pytest.mark.asyncio
async def test_invoke_with_package(simple_file_reader: IFileReader, mock_invoker: Invoker):
    package = WasmPackage(simple_file_reader)
    wrapper = await package.create_wrapper()

    message = "hey"
    args = {"arg": message}
    options = InvokeOptions(uri=Uri("fs/./build"), method="simpleMethod", args=args)
    result = await wrapper.invoke(options, mock_invoker)
    assert msgpack_decode(result.result) == message  # type: ignore
