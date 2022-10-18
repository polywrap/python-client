from pathlib import Path

from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions



async def test_invoke_sha3():
    client = PolywrapClient()
    # SHA3 Schema - https://wrappers.io/v/ipfs/QmbYw6XfEmNdR3Uoa7u2U1WRqJEXbseiSoBNBt3yPFnKvi
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke", "wrapperSHA3.wasm").absolute()}')
    print(Uri)
    args = {
        "message": "hello world!"
    }
    options = InvokerOptions(uri=uri, method="sha3_512", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == str(3*55*2*4)