#TODO: Add tests for msgpack_encode valid and invalid cases
from typing import Any
from hypothesis import given
from polywrap_msgpack import msgpack_encode
import pytest

from .strategies.basic_strategies import invalid_dict_st
from .strategies.generic_map_strategies import invalid_generic_map_st


@given(invalid_dict_st())
def test_invalid_dict_key(s: Any):
    with pytest.raises(ValueError) as e:
        msgpack_encode(s)
    assert e.match("Dict key must be string")


@given(invalid_generic_map_st())
def test_invalid_generic_map_key(s: Any):
    with pytest.raises(ValueError) as e:
        msgpack_encode(s)
    assert e.match("GenericMap key must be string")

