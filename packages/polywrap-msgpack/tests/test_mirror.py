from dataclasses import asdict
from typing import Any, Dict, List, Sequence
from hypothesis import given

from polywrap_msgpack import msgpack_decode, msgpack_encode, GenericMap
from .strategies.basic_strategies import (
    scalar_st,
    sequence_of_scalar_st,
    valid_dict_st,
)
from .strategies.class_strategies import (
    SimpleSlots,
    NestedSlots,
    Simple,
    Nested,
    simple_slots_class_st,
    nested_slots_class_st,
    simple_class_st,
    nested_class_st,
    list_of_nested_class_st,
    dict_of_classes_st,
)
from .strategies.generic_map_strategies import (
    valid_generic_map_st,
)

from .strategies.enum_strategies import enum_st


@given(scalar_st())
def test_mirror_scalar(s: Any):
    assert msgpack_decode(msgpack_encode(s)) == s


@given(enum_st())
def test_mirror_enum(s: Any):
    assert msgpack_decode(msgpack_encode(s)) == s


@given(sequence_of_scalar_st())
def test_mirror_any_sequence_of_scalars(s: Sequence[Any]):
    assert msgpack_decode(msgpack_encode(s)) == list(s)


@given(valid_dict_st())
def test_mirror_valid_dict(s: Dict[str, Any]):
    assert msgpack_decode(msgpack_encode(s)) == s


@given(simple_slots_class_st())
def test_mirror_simple_slots_class(s: SimpleSlots):
    assert msgpack_decode(msgpack_encode(s)) == asdict(s)


@given(nested_slots_class_st())
def test_mirror_nested_slots_class(s: NestedSlots):
    assert msgpack_decode(msgpack_encode(s)) == asdict(s)


@given(simple_class_st())
def test_mirror_simple_class(s: Simple):
    assert msgpack_decode(msgpack_encode(s)) == asdict(s)


@given(nested_class_st())
def test_mirror_nested_class(s: Nested):
    assert msgpack_decode(msgpack_encode(s)) == asdict(s)


@given(list_of_nested_class_st())
def test_mirror_list_of_nested_class(s: List[Nested]):
    assert msgpack_decode(msgpack_encode(s)) == [asdict(x) for x in s]


@given(dict_of_classes_st())
def test_mirror_dict_of_classes(s: Dict[str, Any]):
    assert msgpack_decode(msgpack_encode(s)) == {k: asdict(v) for k, v in s.items()}


@given(valid_generic_map_st())
def test_mirror_valid_generic_map(s: GenericMap[str, Any]):
    assert msgpack_decode(msgpack_encode(s)) == s
