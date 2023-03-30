from pathlib import Path
from polywrap_client import PolywrapClient, PolywrapClientConfig
from polywrap_manifest import deserialize_wrap_manifest
from polywrap_core import Uri, InvokerOptions, FileReader, UriPackageOrWrapper
from polywrap_uri_resolvers import BaseUriResolver, SimpleFileReader, StaticResolver
from polywrap_wasm import WasmWrapper


async def test_invoke(
    client: PolywrapClient,
    simple_file_reader: FileReader,
    simple_wrap_module: bytes,
    simple_wrap_manifest: bytes,
):
    uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke").absolute()}'
    )
    args = {"arg": "hello polywrap"}
    options: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(
        uri=uri, method="simpleMethod", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result == args["arg"]

    manifest = deserialize_wrap_manifest(simple_wrap_manifest)

    wrapper = WasmWrapper(
        file_reader=simple_file_reader,
        wasm_module=simple_wrap_module,
        manifest=manifest,
    )
    resolver = StaticResolver({Uri.from_str("ens/wrapper.eth"): wrapper})

    config = PolywrapClientConfig(resolver=resolver)
    client = PolywrapClient(config=config)

    args = {"arg": "hello polywrap"}
    options = InvokerOptions(
        uri=Uri.from_str("ens/wrapper.eth"),
        method="simpleMethod",
        args=args,
        encode_result=False,
    )
    result = await client.invoke(options)

    assert result == args["arg"]


async def test_subinvoke():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={
            Uri.from_str("ens/add.eth"): Uri.from_str(
                f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "subinvoke").absolute()}'
            ),
        },
    )

    client = PolywrapClient(config=PolywrapClientConfig(resolver=uri_resolver))
    uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "invoke").absolute()}'
    )
    args = {"a": 1, "b": 2}
    options: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(
        uri=uri, method="add", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result == "1 + 2 = 3"


async def test_interface_implementation():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )

    interface_uri = Uri.from_str("ens/interface.eth")
    impl_uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "implementation").absolute()}'
    )

    client = PolywrapClient(
        config=PolywrapClientConfig(
            resolver=uri_resolver, interfaces={interface_uri: [impl_uri]}
        )
    )
    uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "wrapper").absolute()}'
    )
    args = {"arg": {"str": "hello", "uint8": 2}}
    options: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(
        uri=uri, method="moduleMethod", args=args, encode_result=False
    )
    result = await client.invoke(options)
    assert client.get_implementations(interface_uri) == [impl_uri]
    assert result == {"str": "hello", "uint8": 2}


def test_get_env_by_uri():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )
    uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}'
    )
    env = {"externalArray": [1, 2, 3], "externalString": "hello"}

    client = PolywrapClient(
        config=PolywrapClientConfig(
            envs={uri: env},
            resolver=uri_resolver,
        )
    )
    assert client.get_env_by_uri(uri) == env


async def test_env():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )

    uri = Uri.from_str(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}'
    )
    env = {"externalArray": [1, 2, 3], "externalString": "hello"}

    client = PolywrapClient(
        config=PolywrapClientConfig(
            envs={uri: env},
            resolver=uri_resolver,
        )
    )
    options: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(
        uri=uri,
        method="externalEnvMethod",
        args={},
        encode_result=False,
    )

    result = await client.invoke(options)

    assert result == env
