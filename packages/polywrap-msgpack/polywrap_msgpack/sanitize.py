"""This module contains the sanitize function that converts\
    python values into msgpack compatible values."""
from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple, cast

from .extensions.generic_map import GenericMap


def sanitize(value: Any) -> Any:
    """Sanitize the value into msgpack encoder compatible format.

    Args:
        value (Any): any valid python value

    Raises:
        ValueError: when dict key isn't string

    Returns:
        Any: msgpack compatible sanitized value

    Examples:
        >>> sanitize({"a": 1})
        {'a': 1}
        >>> sanitize({1, 2, 3})
        [1, 2, 3]
        >>> sanitize((1, 2, 3))
        [1, 2, 3]
        >>> sanitize([{1}, (2, 3), [4]])
        [[1], [2, 3], [4]]
        >>> class Foo: pass
        >>> foo = Foo()
        >>> foo.bar = 1
        >>> sanitize(foo)
        {'bar': 1}
        >>> sanitize({1: 1})
        Traceback (most recent call last):
        ...
        ValueError: Dict key must be string, got 1 of type <class 'int'>
        >>> sanitize(GenericMap({1: 2}))
        Traceback (most recent call last):
        ...
        ValueError: GenericMap key must be string, got 1 of type <class 'int'>
    """
    if isinstance(value, GenericMap):
        dictionary: Dict[Any, Any] = cast(
            GenericMap[Any, Any], value
        )._map  # pyright: ignore[reportPrivateUsage]
        new_map: GenericMap[str, Any] = GenericMap({})
        for key, val in dictionary.items():
            if not isinstance(key, str):
                raise ValueError(
                    f"GenericMap key must be string, got {key} of type {type(key)}"
                )
            new_map[key] = sanitize(val)
        return new_map
    if isinstance(value, dict):
        dictionary: Dict[Any, Any] = value
        new_dict: Dict[str, Any] = {}
        for key, val in dictionary.items():
            if not isinstance(key, str):
                raise ValueError(
                    f"Dict key must be string, got {key} of type {type(key)}"
                )
            new_dict[key] = sanitize(val)
        return new_dict
    if isinstance(value, list):
        array: List[Any] = value
        return [sanitize(a) for a in array]
    if isinstance(value, tuple):
        array: List[Any] = list(cast(Tuple[Any], value))
        return sanitize(array)
    if isinstance(value, set):
        set_val: List[Any] = list(cast(Set[Any], value))
        return sanitize(set_val)
    if isinstance(value, complex):
        return str(value)
    if hasattr(value, "__slots__"):
        return {
            s: sanitize(getattr(value, s))
            for s in getattr(value, "__slots__")
            if hasattr(value, s)
        }
    if hasattr(value, "__dict__"):
        return {k: sanitize(v) for k, v in cast(Dict[Any, Any], vars(value)).items()}
    return value


__all__ = ["sanitize"]
