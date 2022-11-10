import pytest
from pathlib import Path

from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions, InterfaceImplementations, Env, UriWrapper
from polywrap_uri_resolvers import BaseUriResolver, SimpleFileReader, StaticResolver
from polywrap_result import Result, Ok, Err
from polywrap_client.client import PolywrapClientConfig
from polywrap_wasm import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, IFileReader, WasmWrapper

@pytest.fixture
def simple_wrap_module():
    wrap_path = Path(__file__).parent / "cases" / "simple-invoke" / "wrap.wasm"
    with open(wrap_path, "rb") as f:
        yield f.read()


@pytest.fixture
def simple_wrap_manifest():
    wrap_path = Path(__file__).parent / "cases" / "simple-invoke" / "wrap.info"
    with open(wrap_path, "rb") as f:
        yield f.read()

@pytest.fixture
def simple_file_reader(simple_wrap_module: bytes, simple_wrap_manifest: bytes):
    class FileReader(IFileReader):
        async def read_file(self, file_path: str) -> Result[bytes]:
            if file_path == WRAP_MODULE_PATH:
                return Ok(simple_wrap_module)
            if file_path == WRAP_MANIFEST_PATH:
                return Ok(simple_wrap_manifest)
            return Err.from_str(f"FileNotFound: {file_path}")

    yield FileReader()

@pytest.mark.asyncio
async def test_invoke(
    simple_file_reader: IFileReader,
    simple_wrap_module: bytes,
    simple_wrap_manifest: bytes
):
    client = PolywrapClient()
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke").absolute()}'
    )
    args = {"arg": "hello polywrap"}
    options = InvokerOptions(
        uri=uri, method="simpleMethod", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result.unwrap() == args["arg"]

    wrapper = WasmWrapper(
        file_reader=simple_file_reader, 
        wasm_module=simple_wrap_module, 
        manifest=simple_wrap_manifest
    )
    uri_wrapper = UriWrapper(uri=Uri("ens/wrapper.eth"), wrapper=wrapper)
    resolver = StaticResolver.from_list([uri_wrapper]).unwrap()

    config = PolywrapClientConfig(resolver=resolver)
    client = PolywrapClient(config=config)

    args = {"arg": "hello polywrap"}
    options = InvokerOptions(
        uri=Uri("ens/wrapper.eth"), 
        method="simpleMethod", 
        args=args, 
        encode_result=False
    )
    result = await client.invoke(options)

    assert result.unwrap() == args["arg"]

async def test_subinvoke():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={
            Uri("ens/add.eth"): Uri(
                f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "subinvoke").absolute()}'
            ),
        },
    )

    client = PolywrapClient(config=PolywrapClientConfig(envs=[], resolver=uri_resolver))
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "invoke").absolute()}'
    )
    args = {"a": 1, "b": 2}
    options = InvokerOptions(uri=uri, method="add", args=args, encode_result=False)
    result = await client.invoke(options)

    assert result.unwrap() == "1 + 2 = 3"


async def test_interface_implementation():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )

    impl_uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "implementation").absolute()}'
    )

    client = PolywrapClient(
        config=PolywrapClientConfig(
            envs=[],
            resolver=uri_resolver,
            interfaces=[
                InterfaceImplementations(
                    interface=Uri("ens/interface.eth"), implementations=[impl_uri]
                )
            ],
        )
    )
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "wrapper").absolute()}'
    )
    args = {"arg": {"str": "hello", "uint8": 2}}
    options = InvokerOptions(
        uri=uri, method="moduleMethod", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result.unwrap() == {"str": "hello", "uint8": 2}


async def test_env():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )

    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}')
    env = {"externalArray": [1, 2, 3], "externalString": "hello"}

    client = PolywrapClient(
        config=PolywrapClientConfig(
            envs=[Env(uri=uri, env=env)],
            resolver=uri_resolver,
        )
    )
    options = InvokerOptions(
        uri=uri, method="externalEnvMethod", args={}, encode_result=False
    )
    result = await client.invoke(options)

    assert result.unwrap() == env