# Polywrap Python Client - https://polywrap.io
# SHA3 Wrapper Schema - https://wrappers.io/v/ipfs/QmbYw6XfEmNdR3Uoa7u2U1WRqJEXbseiSoBNBt3yPFnKvi

from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions
import hashlib
import pytest
from Crypto.Hash import keccak, SHAKE128, SHAKE256

client = PolywrapClient()
uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "sha3").absolute()}')

args = {"message": "hello polywrap!"}

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_sha3_512():
    options = InvokerOptions(uri=uri, method="sha3_512", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha512()
    s.update(b"hello polywrap!")
    print(result)
    assert result.result == s.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_sha3_384():
    options = InvokerOptions(uri=uri, method="sha3_384", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha384()
    s.update(b"hello polywrap!")
    assert result.result == s.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_sha3_256():
    options = InvokerOptions(uri=uri, method="sha3_256", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha256()
    s.update(b"hello polywrap!")
    assert result.result == s.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_sha3_224():
    options = InvokerOptions(uri=uri, method="sha3_224", args=args, encode_result=False)
    result = await client.invoke(options)
    s = hashlib.sha224()
    s.update(b"hello polywrap!")
    assert result.result == s.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_keccak_512():
    options = InvokerOptions(uri=uri, method="keccak_512", args=args, encode_result=False)
    result = await client.invoke(options)
    k = keccak.new(digest_bits=512)
    k.update(b'hello polywrap!')
    assert result.result == k.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_keccak_384():
    options = InvokerOptions(uri=uri, method="keccak_384", args=args, encode_result=False)
    result = await client.invoke(options)
    k = keccak.new(digest_bits=384)
    k.update(b'hello polywrap!')
    assert result.result == k.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_keccak_256():
    options = InvokerOptions(uri=uri, method="keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    k = keccak.new(digest_bits=256)
    k.update(b'hello polywrap!')
    assert result.result == k.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_keccak_224():
    options = InvokerOptions(uri=uri, method="keccak_224", args=args, encode_result=False)
    result = await client.invoke(options)
    k = keccak.new(digest_bits=224)
    k.update(b'hello polywrap!')
    assert result.result == k.digest()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_hex_keccak_256():
    options = InvokerOptions(uri=uri, method="hex_keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    k = keccak.new(digest_bits=256)
    k.update(b'hello polywrap!')
    assert result.result == k.hexdigest()

@pytest.mark.skip(reason="buffer keccak must be implemented in python in order to assert")
async def test_invoke_buffer_keccak_256():
    options = InvokerOptions(uri=uri, method="buffer_keccak_256", args=args, encode_result=False)
    result = await client.invoke(options)
    print(result)
    # TODO:  Not sure exactly what this function `buffer_keccak_256` is doing in order to assert it properly
    assert result.result == False

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_shake_256():
    args = {"message": "hello polywrap!", "outputBits":8}
    options = InvokerOptions(uri=uri, method="shake_256", args=args, encode_result=False)
    result = await client.invoke(options)
    s = SHAKE256.new()
    s.update(b"hello polywrap!")
    assert result.result == s.read(8).hex()

@pytest.mark.skip(reason="can't invoke sha3 wrapper due to an error related to wasmtime")
async def test_invoke_shake_128():
    args = {"message": "hello polywrap!", "outputBits":8}
    options = InvokerOptions(uri=uri, method="shake_128", args=args, encode_result=False)
    result = await client.invoke(options)
    s = SHAKE128.new()
    s.update(b"hello polywrap!")
    assert result.result == s.read(8).hex()