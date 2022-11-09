from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple

from polywrap_msgpack import msgpack_decode, msgpack_encode, sanitize
from tests.conftest import DataClassObject, DataClassObjectWithSlots, Example
from polywrap_core import Uri
from pathlib import Path

# ENCODING AND DECODING

def test_msgpack_can_encode_uris():

    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}')
    print(f"{uri}")
    print(f"{type(uri)=}")
    print(f"{uri.uri=}")

    print(f"{uri.__class__=}")
    print(f"{uri.__class__.__name__=}")
    try:
        if uri.__class__.__name__ == 'Uri':
           raise TypeError("Cannot encode Uri")
    except TypeError:
        assert False

def test_encode_and_decode_object():
    custom_object = {"firstKey": "firstValue", "secondKey": "secondValue"}

    encoded = msgpack_encode(custom_object)
    assert encoded == b"\x82\xa8firstKey\xaafirstValue\xa9secondKey\xabsecondValue"

    decoded = msgpack_decode(encoded)
    assert decoded == custom_object


def test_encode_and_decode_instance():
    @dataclass
    class Test:
        firstKey: str
        secondKey: str

        def method(self):
            pass

    custom_object = Test("firstValue", "secondValue")
    encoded = msgpack_encode(custom_object)

    assert encoded == b"\x82\xa8firstKey\xaafirstValue\xa9secondKey\xabsecondValue"

    complex_custom_object_with_class = {"foo": custom_object, "bar": {"foo": "bar"}}

    complex_custom_object_with_dict = {
        "foo": {"firstKey": "firstValue", "secondKey": "secondValue"},
        "bar": {"foo": "bar"},
    }

    encoded_with_dict = msgpack_encode(complex_custom_object_with_dict)
    encoded_with_class = msgpack_encode(complex_custom_object_with_class)

    assert encoded_with_dict == encoded_with_class

    decoded_with_dict = msgpack_decode(encoded_with_dict)

    assert complex_custom_object_with_dict == decoded_with_dict


def test_generic_map_decode():
    encoded = b"\xc7+\x01\x82\xa8firstKey\xaafirstValue\xa9secondKey\xabsecondValue"
    decoded = msgpack_decode(encoded)

    assert decoded == {"firstKey": "firstValue", "secondKey": "secondValue"}


# STRINGS


def test_sanitize_str_returns_same_str():
    assert sanitize("https://docs.polywrap.io/") == "https://docs.polywrap.io/"


def test_sanitized_polywrap_ens_uri():
    assert (
        sanitize("wrap://authority-v2/path.to.thing.root/sub/path")
        == "wrap://authority-v2/path.to.thing.root/sub/path"
    )


# LISTS


def test_sanitize_simple_list_returns_simple_list():
    assert sanitize([1]) == [1]


def test_sanitize_empty_list_returns_empty_list():
    assert sanitize([]) == []


def test_sanitize_long_list_returns_long_list():
    assert sanitize([2, 55, 1234, 6345]) == [2, 55, 1234, 6345]


def test_sanitize_complex_list_returns_list(complex_list: List[Any]):
    assert sanitize(complex_list) == complex_list


def test_sanitize_nested_list_returns_nested_list(nested_list: List[Any]):
    assert sanitize(nested_list) == nested_list


# COMPLEX NUMBERS


def test_sanitize_complex_number_returns_string():
    assert sanitize(3 + 5j) == "(3+5j)"
    assert sanitize(0 + 9j) == "9j"


def test_sanitize_simple_dict_returns_sanitized_values(simple_dict: Dict[str, str]):
    assert sanitize(simple_dict) == simple_dict


# SLOTS


def test_sanitize_object_with_slots_attributes_returns_dict_instead(
    object_with_slots_attributes: Example, object_with_slots_sanitized: Dict[str, str]
):
    assert sanitize(object_with_slots_attributes) == object_with_slots_sanitized


# TUPLES


def test_sanitize_single_tuple_returns_list(single_tuple: Tuple[int]):
    # To create a tuple with only one item, you have add a comma after the item,
    # otherwise Python will not recognize the variable as a tuple.
    assert type(sanitize(single_tuple)) == list
    assert sanitize(single_tuple) == [8]


def test_sanitize_long_tuple_returns_list():
    assert sanitize((2, 3, 6)) == [2, 3, 6]


def test_sanitize_nested_tuples_returns_nested_list(
    nested_tuple: Tuple[Any, ...], nested_list: List[Any]
):
    assert sanitize(nested_tuple) == nested_list


# SETS


def test_sanitize_set_returns_list(set1: Set[Any]):
    # Remember sets automatically reorganize the contents of the object
    # meaning {'bob', 'alice'} might be stored as ['alice','bob'] once sanitized
    assert type(sanitize(set1)) == list
    assert sanitize(set1) == list(set1)


def test_sanitize_set_returns_list_with_all_items_of_the_set(
    set1: Set[Any], set2: Set[Any]
):
    sanitized = sanitize(set1)
    # r: List[bool] = []
    assert list(set1) == sanitized
    # [r.append(True) if item in sanitized else r.append(False) for item in set1]
    # assert False not in r

    sanitized = sanitize(set2)
    assert list(set2) == sanitized
    # r = []
    # [r.append(True) if item in sanitized else r.append(False) for item in set2]
    # assert False not in r


def test_sanitize_set_returns_list_of_same_length(set1: Set[Any]):
    assert len(sanitize(set1)) == len(set1)


def test_sanitize_complex_dict_returns_sanitized_values():
    complex_dict = {
        "name": ["John", "Doe"],
        "position": [-0.34478, 12.98453],
        "color": "green",
        "age": 33,
        "origin": (0, 0),
        "is_online": True,
        "pet": None,
        "friends": {"bob", "alice", "megan", "john"},
    }
    sanitized_complex_dict = {
        "name": ["John", "Doe"],
        "position": [-0.34478, 12.98453],
        "color": "green",
        "age": 33,
        "origin": [0, 0],
        "is_online": True,
        "pet": None,
        "friends": ["alice", "bob", "john", "megan"],
    }

    complex_dict = sanitize(complex_dict)
    friends = sorted(complex_dict["friends"])
    complex_dict["friends"] = friends

    assert sanitize(complex_dict) == sanitized_complex_dict


# DATA CLASSES


def test_sanitize_dataclass_object_returns_dict(
    dataclass_object1: DataClassObject, dataclass_object1_as_dict: Dict[str, Any]
):
    assert sanitize(dataclass_object1) == dataclass_object1_as_dict


def test_sanitize_list_of_dataclass_objects_returns_list_of_dicts(
    dataclass_object1: DataClassObject, dataclass_object2: DataClassObject
):
    assert sanitize([dataclass_object1, dataclass_object2]) == [
        dataclass_object1.__dict__,
        dataclass_object2.__dict__,
    ]


def test_sanitize_dict_of_dataclass_objects_returns_dict_of_dicts(
    dataclass_object1: DataClassObject, dataclass_object2: DataClassObject
):
    assert sanitize(
        {"firstKey": dataclass_object1, "secondKey": dataclass_object2}
    ) == {
        "firstKey": dataclass_object1.__dict__,
        "secondKey": dataclass_object2.__dict__,
    }


# DATA CLASSES WITH SLOTS


def test_sanitize_dataclass_objects_with_slots_returns_dict(
    dataclass_object_with_slots1: DataClassObjectWithSlots,
    dataclass_object_with_slots1_sanitized: Dict[str, Any],
):
    sanitize(dataclass_object_with_slots1)
    assert (
        sanitize(dataclass_object_with_slots1) == dataclass_object_with_slots1_sanitized
    )


def test_sanitize_list_of_dataclass_objects_with_slots_returns_list_of_dicts(
    dataclass_object_with_slots1: DataClassObjectWithSlots,
    dataclass_object_with_slots2: DataClassObjectWithSlots,
    dataclass_object_with_slots1_sanitized: Dict[str, Any],
    dataclass_object_with_slots2_sanitized: Dict[str, Any],
):
    assert sanitize([dataclass_object_with_slots1, dataclass_object_with_slots2]) == [
        dataclass_object_with_slots1_sanitized,
        dataclass_object_with_slots2_sanitized,
    ]


def test_sanitize_dict_of_dataclass_objects_with_slots_returns_list_of_dicts(
    dataclass_object_with_slots1: DataClassObjectWithSlots,
    dataclass_object_with_slots2: DataClassObjectWithSlots,
    dataclass_object_with_slots1_sanitized: Dict[str, Any],
    dataclass_object_with_slots2_sanitized: Dict[str, Any],
):
    assert sanitize(
        {
            "firstKey": dataclass_object_with_slots1,
            "secondKey": dataclass_object_with_slots2,
        }
    ) == {
        "firstKey": dataclass_object_with_slots1_sanitized,
        "secondKey": dataclass_object_with_slots2_sanitized,
    }
