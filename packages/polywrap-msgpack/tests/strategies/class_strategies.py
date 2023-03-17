from hypothesis import strategies as st

from dataclasses import dataclass
from typing import Any, Dict, List

from .basic_strategies import scalar_st


@dataclass(slots=True)
class SimpleSlots:
    x: Any
    y: Any


@dataclass(slots=True)
class NestedSlots:
    a: Any
    b: SimpleSlots


@dataclass
class Simple:
    x: Any
    y: Any


@dataclass
class Nested:
    a: Any
    b: Simple


def simple_slots_class_st() -> st.SearchStrategy[SimpleSlots]:
    """Define a strategy for generating the `SimpleSlots` class.

    Examples:
        >>> SimpleSlots(1, 2)
        >>> SimpleSlots(1.0, 2.0)
        >>> SimpleSlots(True, False)
        >>> SimpleSlots(None, "abc")
        >>> SimpleSlots("abc", "def")
        >>> SimpleSlots(b"abc", 12)
        >>> SimpleSlots(b"abc", b"def")
    """
    return st.builds(SimpleSlots, scalar_st(), scalar_st())


def nested_slots_class_st() -> st.SearchStrategy[NestedSlots]:
    """Define a strategy for generating the `Nested` class.

    Examples:
        >>> Nested(1, SimpleSlots(2, 3))
        >>> Nested(1.0, SimpleSlots(2.0, 3.0))
        >>> Nested(True, SimpleSlots(True, False))
        >>> Nested(None, SimpleSlots(None, "abc"))
        >>> Nested("abc", SimpleSlots("abc", "def"))
        >>> Nested(b"abc", SimpleSlots(b"abc", 12))
        >>> Nested(b"abc", SimpleSlots(b"abc", b"def"))
    """
    return st.builds(NestedSlots, scalar_st(), simple_slots_class_st())


def simple_class_st() -> st.SearchStrategy[Simple]:
    """Define a strategy for generating the `Simple` class.

    Examples:
        >>> Simple(1, 2)
        >>> Simple(1.0, 2.0)
        >>> Simple(True, False)
        >>> Simple(None, "abc")
        >>> Simple("abc", "def")
        >>> Simple(b"abc", 12)
        >>> Simple(b"abc", b"def")
    """
    return st.builds(Simple, scalar_st(), scalar_st())


def nested_class_st() -> st.SearchStrategy[Nested]:
    """Define a strategy for generating the `Nested` class.

    Examples:
        >>> Nested(1, Simple(2, 3))
        >>> Nested(1.0, Simple(2.0, 3.0))
        >>> Nested(True, Simple(True, False))
        >>> Nested(None, Simple(None, "abc"))
        >>> Nested("abc", Simple("abc", "def"))
        >>> Nested(b"abc", Simple(b"abc", 12))
        >>> Nested(b"abc", Simple(b"abc", b"def"))
    """
    return st.builds(Nested, scalar_st(), simple_class_st())


def list_of_nested_class_st() -> st.SearchStrategy[List[Nested]]:
    """Define a strategy for generating a list of `Nested` class.

    Examples:
        >>> []
        >>> [Nested(1, Simple(2, 3))]
        >>> [Nested(1.0, Simple(2.0, 3.0))]
        >>> [Nested(True, Simple(True, False))]
        >>> [Nested(None, Simple(None, "abc"))]
        >>> [Nested("abc", Simple("abc", "def"))]
        >>> [Nested(b"abc", Simple(b"abc", 12))]
        >>> [Nested(b"abc", Simple(b"abc", b"def"))]
    """
    return st.lists(nested_class_st(), min_size=1, max_size=10)


def dict_of_classes_st() -> st.SearchStrategy[Dict[str, Any]]:
    """Define a strategy for generating a dict of `Simple` class.

    Examples:
        >>> {}
        >>> {"a": Simple(1, 2), "b": NestedSlots(1, Simple(2, 3))}
        >>> {"a": Simple(1.0, 2.0)}
        >>> {"a": Nested(b"abc", Simple(b"abc", 12))}
        >>> {"a": Simple(b"abc", b"def")}
        >>> {"a": Simple(None, "abc"), "b": NestedSlots(13, Simple("abc", 3))}

    """
    return st.dictionaries(st.text(), st.one_of(simple_class_st(), nested_slots_class_st()), min_size=1, max_size=10)