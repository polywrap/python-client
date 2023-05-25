# import pytest
# from pathlib import Path

# from polywrap_result import Ok, Err, Result
# from polywrap_wasm import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, IFileReader, WasmPackage, WasmWrapper
# from polywrap_core import UriPackage, Uri, UriResolutionContext, UriWrapper, IWrapPackage
# from polywrap_client import PolywrapClient
# from polywrap_uri_resolvers import StaticResolver
# from polywrap_manifest import deserialize_wrap_manifest


# @pytest.fixture
# def simple_wrap_module():
#     wrap_path = Path(__file__).parent / "cases" / "simple" / "wrap.wasm"
#     with open(wrap_path, "rb") as f:
#         yield f.read()


# @pytest.fixture
# def simple_wrap_manifest():
#     wrap_path = Path(__file__).parent / "cases" / "simple" / "wrap.info"
#     with open(wrap_path, "rb") as f:
#         yield f.read()

# @pytest.fixture
# def simple_file_reader(simple_wrap_module: bytes, simple_wrap_manifest: bytes):
#     class FileReader(IFileReader):
#         async def read_file(self, file_path: str) -> Result[bytes]:
#             if file_path == WRAP_MODULE_PATH:
#                 return Ok(simple_wrap_module)
#             if file_path == WRAP_MANIFEST_PATH:
#                 return Ok(simple_wrap_manifest)
#             return Err.from_str(f"FileNotFound: {file_path}")

#     yield FileReader()

# @pytest.mark.asyncio
# async def test_static_resolver(
#     simple_file_reader: IFileReader,
#     simple_wrap_module: bytes,
#     simple_wrap_manifest: bytes
# ):
#     package = WasmPackage(simple_file_reader)

#     manifest = deserialize_wrap_manifest(simple_wrap_manifest).unwrap()
#     wrapper = WasmWrapper(simple_file_reader, simple_wrap_module, manifest)

#     uri_wrapper = UriWrapper(uri=Uri("ens/wrapper.eth"), wrapper=wrapper)
#     uri_package = UriPackage(uri=Uri("ens/package.eth"), package=package)

#     resolver = StaticResolver.from_list([ uri_package, uri_wrapper, [
#         UriPackage(uri=Uri("ens/nested-package.eth"), package=package)
#     ]]).unwrap()

#     resolution_context = UriResolutionContext()
#     result = await resolver.try_resolve_uri(Uri("ens/package.eth"), PolywrapClient(), resolution_context)

#     assert result.is_ok
#     assert isinstance((result.unwrap()).package, IWrapPackage)

#     result = await resolver.try_resolve_uri(Uri("ens/wrapper.eth"), PolywrapClient(), resolution_context)

#     assert result.is_ok
#     assert isinstance((result.unwrap()).wrapper, WasmWrapper)

#     result = await resolver.try_resolve_uri(Uri("ens/nested-package.eth"), PolywrapClient(), resolution_context)

#     assert result.is_ok
#     assert isinstance((result.unwrap()).package, IWrapPackage)

