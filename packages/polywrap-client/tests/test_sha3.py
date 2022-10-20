# Polywrap Python Client - https://polywrap.io
# SHA3 Wrapper Schema - https://wrappers.io/v/ipfs/QmbYw6XfEmNdR3Uoa7u2U1WRqJEXbseiSoBNBt3yPFnKvi

from mailbox import _mboxMMDFMessage
from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions
import hashlib
import sha3

client = PolywrapClient()
uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke", "wrapperSHA3.wasm").absolute()}')

args = {"message": "hello polywrap!"}

async def test_invoke_sha3_512():
    options = InvokerOptions(uri=uri, method="sha3_512", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha512()
    s.update(b"hello polywrap!")
    assert result.result == s.hexdigest()

async def test_invoke_sha3_384():
    options = InvokerOptions(uri=uri, method="sha3_384", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha384()
    s.update(b"hello polywrap!")
    assert result.result == s.hexdigest()


async def test_invoke_sha3_256():
    options = InvokerOptions(uri=uri, method="sha3_256", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha256()
    s.update(b"hello polywrap!")
    assert result.result == s.hexdigest()


async def test_invoke_sha3_224():
    options = InvokerOptions(uri=uri, method="sha3_224", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha224()
    s.update(b"hello polywrap!")
    assert result.result == s.hexdigest()


async def test_invoke_keccak_512():
    options = InvokerOptions(uri=uri, method="keccak_512", args=args, encode_result=False)
    result = await client.invoke(options)
    k = hashlib.sha512()
    k.update(b"hello polywrap!")
    assert result.result == False


async def test_invoke_keccak_384():
    options = InvokerOptions(uri=uri, method="keccak_384", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_keccak_256():
    options = InvokerOptions(uri=uri, method="keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_keccak_224():
    options = InvokerOptions(uri=uri, method="keccak_224", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_hex_keccak_256():
    options = InvokerOptions(uri=uri, method="hex_keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_buffer_keccak_256():
    options = InvokerOptions(uri=uri, method="buffer_keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_shake_256():
    args = {"message": "hello polywrap!", "outputBits":2022}
    options = InvokerOptions(uri=uri, method="shake_256", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False

async def test_invoke_shake_128():
    args = {"message": "hello polywrap!", "outputBits":2022}
    options = InvokerOptions(uri=uri, method="shake_128", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    assert result.result == False