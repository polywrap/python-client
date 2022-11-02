# Polywrap Python Client - https://polywrap.io
# bigint_type_rs wrapper schema - https://github.com/polywrap/toolchain/blob/origin-0.10-dev/packages/test-cases/cases/wrappers/wasm-rs/bigint-type/schema.graphql

from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions

@pytest.mark.skip(reason="can't invoke bigint-rs wrapper due to an error related to wasmtime")
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

@pytest.mark.skip(reason="can't invoke bigint-rs wrapper due to an error related to wasmtime")
async def test_invoke_bigint_rs_with_1arg_and_2prop():
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

@pytest.mark.skip(reason="can't invoke bigint-rs wrapper due to an error related to wasmtime")
async def test_invoke_bigint_rs_with_2arg_and_1prop():
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

#@pytest.mark.skip(reason="can't invoke bigint-rs wrapper due to an error related to wasmtime")
async def test_invoke_bigint_rs_with_2arg_and_2prop():
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
    print(result.unwrap())
    assert result.unwrap() == str(123123*555*1000*4)