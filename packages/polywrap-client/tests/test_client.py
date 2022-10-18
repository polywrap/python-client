from pathlib import Path

from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions
from polywrap_uri_resolvers import BaseUriResolver, SimpleFileReader

from polywrap_client.client import PolywrapClientConfig


async def test_invoke():
    client = PolywrapClient()
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke", "wrap.wasm").absolute()}'
    )
    args = {"arg": "hello polywrap"}
    options = InvokerOptions(
        uri=uri, method="simpleMethod", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result.result == args["arg"]


async def test_subinvoke():
    uri_resolver = BaseUriResolver(
        file_reader=SimpleFileReader(),
        redirects={
            Uri("ens/add.eth"): Uri(
                f'fs/{Path(__file__).parent.joinpath("cases", "subinvoke", "wrap-subinvoke.wasm").absolute()}'
            ),
        },
    )

    client = PolywrapClient(config=PolywrapClientConfig(
        envs=[], resolver=uri_resolver
    ))
    uri = Uri(
        f'fs/{Path(__file__).parent.joinpath("cases", "subinvoke", "wrap-invoke.wasm").absolute()}'
    )
    args = b'\x82\xa1a\x01\xa1b\x02'
    options = InvokerOptions(
        uri=uri, method="add", args=args, encode_result=False
    )
    result = await client.invoke(options)

    assert result.result == "1 + 2 = 3"


async def test_invoke_bignumber_1arg_and_1prop():
    client = PolywrapClient()
    # BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke" ,"wrapperBigNumber.wasm").absolute()}')
    args = { "arg1": "123", # The base number
        "obj": {
            "prop1": "1000", # multiply the base number by this factor
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == "123000"

async def test_invoke_bignumber_with_1arg_and_2props():
    client = PolywrapClient()
    # BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke" ,"wrapperBigNumber.wasm").absolute()}')
    args = {
        "arg1": "123123",
        "obj": {
            "prop1": "1000",
           "prop2": "4"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == str(123123*1000*4)

async def test_invoke_bignumber_with_2args_and_1prop():
    client = PolywrapClient()
    # BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke" ,"wrapperBigNumber.wasm").absolute()}')
    args = {
        "arg1": "123123",
        "obj": {
            "prop1": "1000",
           "prop2": "444"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == str(123123*1000*444)

async def test_invoke_bignumber_with_2args_and_2props():
    client = PolywrapClient()
    # BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke" ,"wrapperBigNumber.wasm").absolute()}')
    args = {
        "arg1": "123123",
        "arg2": "555",
        "obj": {
            "prop1": "1000",
           "prop2": "4"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == str(123123*555*1000*4)
