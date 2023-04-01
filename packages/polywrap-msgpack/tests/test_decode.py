from typing import List, NamedTuple, Type

from msgpack import FormatError, StackError
from polywrap_msgpack import msgpack_decode, MsgpackDecodeError
import pytest

class InvalidEncodedDataCase(NamedTuple):
    encoded: bytes
    error: Type[Exception]


INVALID_ENCODED_DATA: List[InvalidEncodedDataCase] = [
    InvalidEncodedDataCase(b"\xd9\x97#DL_", ValueError),  # raw8 - length=0x97
    InvalidEncodedDataCase(b"\xc1", FormatError),  # (undefined tag)
    InvalidEncodedDataCase(b"\x91\xc1", FormatError),  # fixarray(len=1) [ (undefined tag) ]
    InvalidEncodedDataCase(
        b"\x91" * 3000,
        StackError,
    ),  # nested fixarray(len=1)
]


@pytest.mark.parametrize("encoded,error", INVALID_ENCODED_DATA)
def test_invalid_encoded_data(encoded: bytes, error: Type[Exception]):
    with pytest.raises(MsgpackDecodeError) as e:
        msgpack_decode(encoded)
    assert e.match("Failed to decode msgpack data")
    assert e.value.__cause__ is not None
    assert e.value.__cause__.__class__ is error
