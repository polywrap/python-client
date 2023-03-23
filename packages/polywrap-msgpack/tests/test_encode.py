from typing import Any
from hypothesis import given
from polywrap_msgpack import msgpack_encode, MsgpackSanitizeError
import pytest

from .strategies.basic_strategies import invalid_dict_st
from .strategies.generic_map_strategies import invalid_generic_map_st


@given(invalid_dict_st())
def test_invalid_dict_key(s: Any):
    with pytest.raises(MsgpackSanitizeError) as e:
        msgpack_encode(s)
    assert e.match("Failed to sanitize object")
    assert e.value.__cause__ is not None
    assert e.value.__cause__.__class__ is ValueError
    assert e.value.__cause__.args[0].startswith("Dict key must be string")


@given(invalid_generic_map_st())
def test_invalid_generic_map_key(s: Any):
    with pytest.raises(MsgpackSanitizeError) as e:
        msgpack_encode(s)
    assert e.match("Failed to sanitize object")
    assert e.value.__cause__ is not None
    assert e.value.__cause__.__class__ is ValueError
    assert e.value.__cause__.args[0].startswith("GenericMap key must be string")
