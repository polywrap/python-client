from hypothesis import strategies as st
from typing import Any, cast

from polywrap_msgpack import GenericMap

from .basic_strategies import (
    invalid_dict_key_st,
    invalid_dict_value_st,
    valid_dict_st,
    valid_dict_value_st,
)

# Define a strategy for generating invalid dicts
def invalid_generic_map_st() -> st.SearchStrategy[GenericMap[Any, Any]]:
    """Define a strategy for generating invalid `GenericMap`.

    An invalid `GenericMap` can be any mapping with non-string as keys

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
    return cast(
        st.SearchStrategy[GenericMap[Any, Any]],
        st.builds(
            GenericMap,
            st.one_of(
                st.dictionaries(invalid_dict_key_st(), valid_dict_value_st()),
                st.dictionaries(
                    st.text(),
                    cast(
                        st.SearchStrategy[GenericMap[Any, Any]],
                        st.builds(GenericMap, invalid_dict_value_st()),
                    ),
                ),
            ).filter(lambda d: d != {}),
        ),
    )


# Define a strategy for generating valid dicts
def valid_generic_map_st() -> st.SearchStrategy[GenericMap[Any, Any]]:
    """Define a strategy for generating valid `GenericMap`.

    A valid `GenericMap` can be any mapping with only string as keys

    Examples:
        >>> {}
        >>> {"a": 1}
        >>> {"a": 1, "b": 2}
        >>> {"a": 1.8, "b": ["x", "y", "z"], "c": {"d": 3}}}
    """
    return cast(
        st.SearchStrategy[GenericMap[Any, Any]],
        st.builds(GenericMap, valid_dict_st()),
    )
