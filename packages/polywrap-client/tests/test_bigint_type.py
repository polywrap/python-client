# Polywrap Python Client - https://polywrap.io
# BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD

from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions

async def test_invoke_bigint_rs_with_1arg_and_1prop():
    client = PolywrapClient()
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "bigint-type-rs").absolute()}')
    args = { "arg1": "123", # The base number
        "obj": {
            "prop1": "1000", # multiply the base number by this factor
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    assert result.unwrap() == "123000"

async def test_invoke_bignumber_with_1arg_and_2props():
    client = PolywrapClient()
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "bigint-type-rs").absolute()}')
    args = {
        "arg1": "123123",
        "obj": {
            "prop1": "1000",
           "prop2": "4"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    assert result.unwrap() == str(123123*1000*4)

async def test_invoke_bignumber_with_2args_and_1prop():
    client = PolywrapClient()
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "bigint-type-rs").absolute()}')
    args = {
        "arg1": "123123",
        "obj": {
            "prop1": "1000",
           "prop2": "444"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    assert result.unwrap() == str(123123*1000*444)

async def test_invoke_bignumber_with_2args_and_2props():
    client = PolywrapClient()
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "bigint-type-rs").absolute()}')
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
    assert result.unwrap() == str(123123*555*1000*4)

async def test_invoke_bignumber_with_2args_and_2props_floats():
    client = PolywrapClient()
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "bigint-type-rs").absolute()}')
    args = {
        "arg1": "123.123",
        "arg2": "55.5",
        "obj": {
            "prop1": "10.001",
           "prop2": "4"
        }
    }
    options = InvokerOptions(uri=uri, method="method", args=args, encode_result=False)
    result = await client.invoke(options)
    assert result.unwrap() == str(123.123*55.5*10.001*4)