from typing import Any, Dict, List, Sequence, Set, Tuple
from hypothesis import strategies as st

from ..consts import C_LONG_MIN, C_LONG_MAX

scalar_st_list = [
    st.none(),
    st.booleans(),
    st.integers(min_value=C_LONG_MIN, max_value=C_LONG_MAX),
    st.floats(allow_nan=False),
    st.text(),
    st.binary(),
]


def scalar_st() -> st.SearchStrategy[Any]:
    """Define a strategy for generating scalars.

    Examples:
        >>> None
        >>> True
        >>> False
        >>> 1
        >>> 1.0
        >>> "a"
        >>> b"abc"
    """
    return st.one_of(*scalar_st_list)


# Define list of scaler strategy
def array_of_scalar_st() -> st.SearchStrategy[List[Any]]:
    """Define a strategy for generating array of scalars.

    This strategy will always generate a list of scalars with same type.

    Examples:
        >>> []
        >>> [1, 2, 3]
        >>> [1.0, 2.0, 3.0]
        >>> ["a", "b", "c"]
        >>> [True, False, True, False]
        >>> [None, None, None]
        >>> [b"abc", b"def", b"ghi"]
    """
    return st.one_of(*[st.lists(s, max_size=10) for s in scalar_st_list])

def tuple_of_scalar_st() -> st.SearchStrategy[Tuple[Any, ...]]:
    """Define a strategy for generating tuple of scalars.

    This strategy will always generate a tuple of scalars with same type.

    Examples:
        >>> ()
        >>> (1, 2, 3)
        >>> (1.0, 2.0, 3.0)
        >>> ("a", "b", "c")
        >>> (True, False, True, False)
        >>> (None, None, None)
        >>> (b"abc", b"def", b"ghi")
    """
    return array_of_scalar_st().map(lambda x: tuple(x))


def set_of_scalar_st() -> st.SearchStrategy[Set[Any]]:
    """Define a strategy for generating set of scalars.

    This strategy will always generate a set of scalars with same type.

    Examples:
        >>> set()
        >>> {1, 2, 3}
        >>> {1.0, 2.0, 3.0}
        >>> {"a", "b", "c"}
        >>> {True, False, True, False}
        >>> {None, None, None}
        >>> {b"abc", b"def", b"ghi"}
    """
    return st.one_of(*[st.sets(s, max_size=10) for s in scalar_st_list])


def sequence_of_scalar_st() -> st.SearchStrategy[Sequence[Any]]:
    """Define a strategy for generating sequence of scalars.

    This strategy will always generate a sequence of scalars with same type.

    Examples:
        >>> []
        >>> ()
        >>> set()
        >>> [1, 2, 3]
        >>> (1.0, 2.0, 3.0)
        >>> {"a", "b", "c"}
        >>> [True, False, True, False]
        >>> (None, None, None)
        >>> {b"abc", b"def", b"ghi"}
    """
    return st.one_of(array_of_scalar_st(), tuple_of_scalar_st(), set_of_scalar_st())

# Define a strategy for generating invalid dict keys
def invalid_dict_key_st() -> st.SearchStrategy[Any]:
    """Define a strategy for generating invalid dict keys.

    A valid dict key must be a UTF-8 encoded string type.

    Examples:
        >>> 1
        >>> 1.0
        >>> True
        >>> False
        >>> None
        >>> b"abc"
    """
    return st.one_of(st.integers(), st.floats(), st.booleans(), st.none(), st.binary())


# Define a strategy for generating valid dict values
def valid_dict_value_st() -> st.SearchStrategy[Any]:
    """Define a strategy for generating valid dict values.

    A valid dict value can be any dictionary with string as keys

    Examples:
        >>> {}
        >>> {"a": 1}
        >>> {"a": 1, "b": 2}
        >>> {"a": 1.8, "b": ["x", "y", "z"], "c": {"d": 3}}}
    """
    return st.recursive(
        st.one_of(scalar_st(), array_of_scalar_st()),
        lambda children: st.lists(children) | st.dictionaries(st.text(), children),
        max_leaves=5,
    )


def invalid_dict_value_st() -> st.SearchStrategy[Dict[Any, Any]]:
    """Define a strategy for generating invalid dict values.

    An invalid dict value can be any dictionary with non-string as keys

    Examples:
        >>> {1: 1}
        >>> {1.0: 1}
        >>> {True: 1}
        >>> {False: 1}
        >>> {None: 1}
        >>> {b"abc": 1}
    """
    return st.dictionaries(invalid_dict_key_st(), scalar_st(), max_size=10).filter(lambda d: d != {})


# Define a strategy for generating invalid dicts
def invalid_dict_st() -> st.SearchStrategy[Dict[Any, Any]]:
    """Define a strategy for generating invalid dicts.

    An invalid dict can be any dictionary with non-string as keys

    Examples:
        >>> {1: 1}
        >>> {1.0: 1}
        >>> {True: 1}
        >>> {False: 1}
        >>> {None: 1}
        >>> {b"abc": 1}
        >>> {"a": 1, {1: 4}, [1.2, 3.4, 5.6]}
        >>> {None: 1, None: 2}
        >>> {b"abc": 1, b"def": 2}
    """
    return st.one_of(
        st.dictionaries(invalid_dict_key_st(), valid_dict_value_st()),
        st.dictionaries(st.text(), invalid_dict_value_st()),
    ).filter(lambda d: d != {})


# Define a strategy for generating valid dicts
def valid_dict_st() -> st.SearchStrategy[Dict[str, Any]]:
    """Define a strategy for generating valid dicts.

    A valid dict can be any dictionary with string as keys

    Examples:
        >>> {}
        >>> {"a": 1}
        >>> {"a": 1, "b": 2}
        >>> {"a": 1.8, "b": ["x", "y", "z"], "c": {"d": 3}}}
    """
    return st.dictionaries(st.text(), valid_dict_value_st())
