from pathlib import Path
import pytest
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions
from polywrap_uri_resolvers import BaseUriResolver, SimpleFileReader
from polywrap_result import Ok
from polywrap_client.polywrap_client import PolywrapClientConfig


async def test_invoke():
    client = PolywrapClient()
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke").absolute()}'
    )
    args = {"arg": "hello polywrap"}
    options = InvokerOptions(
        uri=uri, method="simpleMethod", args=args, encode_result=False, env={}
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
    options = InvokerOptions(uri=uri, method="add", args=args, env={}, encode_result=False)
    result = await client.invoke(options)

    assert result.unwrap() == "1 + 2 = 3"


async def test_interface_implementation():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={},
    )

    interface_uri = Uri("ens/interface.eth")
    impl_uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "implementation").absolute()}'
    )

    client = PolywrapClient(
        config=PolywrapClientConfig(
            envs={},
            resolver=uri_resolver,
            interfaces= {interface_uri : [impl_uri]}
        )
    )
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "wrapper").absolute()}'
    )
    args = {"arg": {"str": "hello", "uint8": 2}}
    options = InvokerOptions(
        uri=uri, method="moduleMethod", args=args, encode_result=False, env={}
    )
    result = await client.invoke(options)
    assert client.get_implementations(interface_uri) == Ok([impl_uri])
    assert result.unwrap() == {"str": "hello", "uint8": 2}


def test_get_env_by_uri():
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
        )
    )
    assert client.get_env_by_uri(uri) == env

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
        )
    )
    print(f"--> Begin by configuring the client with the env: {env}")
    options = InvokerOptions(
        uri=uri, method="externalEnvMethod", args={}, encode_result=False, 
    )

    result = await client.invoke(options)

    assert result.unwrap() == env
