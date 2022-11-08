from pathlib import Path

from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions, InterfaceImplementations, Env
from polywrap_uri_resolvers import BaseUriResolver, SimpleFileReader

from polywrap_client.client import PolywrapClientConfig


async def test_invoke():
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


async def test_subinvoke():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={
            Uri("ens/add.eth"): Uri(
                f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "subinvoke").absolute()}'
            ),
        },
    )

    client = PolywrapClient(config=PolywrapClientConfig(envs={}, interfaces={}, resolver=uri_resolver))
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
            envs={},
            interfaces={
                    InterfaceImplementations(
                        interface=Uri("ens/interface.eth"), implementations=[impl_uri]
                    )
                },
            resolver=uri_resolver,
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
            envs={uri: env},
            resolver=uri_resolver,
            interfaces={}
        )
    )
    options = InvokerOptions(
        uri=uri, method="externalEnvMethod", args={}, encode_result=False
    )
    print(client._config__)
    result = await client.invoke(options)

    assert result.unwrap() == env
